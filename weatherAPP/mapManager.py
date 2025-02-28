import tkinter as tk
from PIL import Image, ImageTk
import utilitairesPays
from pyproj import Transformer

image_path = 'weatherAPP/im.png'
image = Image.open(image_path)
img_width, img_height = image.size


smallSize = 0.2
fullSize =1

class interactiveMap(tk.Canvas):
    def __init__(self, parent, **kwargs):
        
        super().__init__(parent, **kwargs)

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        
        image_path = 'weatherAPP/im.png'
        self.image = Image.open(image_path)
        self.img_width, self.img_height = image.size
        tk_image = ImageTk.PhotoImage(image)
        
        
        # Define a projection system (e.g., Mercator)
        self.config( width =img_width , height=img_height)
        
        self.point = None#
        self.point_position = None

        # Add the image to the canvas
        self.photo = self.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.resize(fullSize)
        
        '''data = utilitairesPays.getSpecificCityInformation("tokyo")
        lat, lng = data["latitude"],data["longitude"]
        x,y = wgs84_to_pixel(lng,lat)
        self.createDot(x,y)
        print("orignial ccorrdinates: ", lat ,"  ",lng)
        longi,lati = pixel_to_wgs84(x,y)
        print("modified ccorrdinates: ", lati ,"  ",longi)
        
        print("canada:    ",utilitairesPays.get_country_code(lat,lng))
        '''
        
    def on_click(self, event):
        # Example: Draw a red dot where the user clicks
        x, y = event.x, event.y
        self.createDot(x,y)
        #print(x ,"  ", y)    
    
    
    def on_enter(self,event):
        self.resize(fullSize)
        #app.geometry("600x1000")
        
    def on_leave(self,event):
        self.resize(smallSize)
        #app.geometry("600x500")    
    
    def createDot(self,pixel_x,pixel_y):
        self.deletePoint()
        dot_radius = 2
        self.point = self.create_oval(pixel_x - dot_radius, pixel_y - dot_radius, 
                        pixel_x + dot_radius, pixel_y + dot_radius, fill='red')   
        self.point_position = (pixel_x, pixel_y)
    
    def deletePoint(self):
        self.delete(self.point)


    def clear_canvas(self):
        self.delete("all")
    
    def resize(self, factor):
        # Calculate new dimensions based on the resize factor
        new_width = int(self.img_width * factor)
        new_height = int(self.img_height * factor)
        
        # Resize the image with the new dimensions
        resized_image = self.image.resize((new_width, new_height), Image.ADAPTIVE)
        
        # Update the canvas configuration
        self.config(width=new_width, height=new_height)
        
        # Create a new PhotoImage object for the resized image
        self.tk_image = ImageTk.PhotoImage(resized_image)
        
        # Delete the old image from the canvas
        self.delete(self.photo)
        
        # Add the resized image to the canvas
        self.photo = self.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
    
        if self.point_position:
            self.redraw_point()

    
    def redraw_point(self):
        if self.point_position:
            pixel_x, pixel_y = self.point_position
            self.createDot(pixel_x, pixel_y)
            #print("=======================redrawing dot==========================")

def get_central_coordinates(country_data):
    north = country_data['north']
    south = country_data['south']
    east = country_data['east']
    west = country_data['west']

    central_latitude = (north + south) / 2
    central_longitude = (east + west) / 2
    
    return wgs84_to_pixel(central_latitude, central_longitude)

def isPointInsideBoundingBox(country_data,point_pixel):
    if not point_pixel:
        print("no point is present")
        return False
    north = country_data['north']
    south = country_data['south']
    east = country_data['east']
    west = country_data['west']

    top_left = wgs84_to_pixel(west, north)
    bottom_right = wgs84_to_pixel(east, south)

    # Unpack coordinates
    top_left_x, top_left_y = top_left
    bottom_right_x, bottom_right_y = bottom_right
    point_x, point_y = point_pixel
    
    # Check if the point is within the bounding box
    if top_left_x <= point_x <= bottom_right_x and bottom_right_y <= point_y <= top_left_y:
        return True
    else:
        return False

def wgs84_to_pixel(lon, lat):

    min_lon, max_lat = -180, 85  # Top-Left (Longitude, Latitude)
    max_lon, min_lat = 180, -85  # Bottom-Right (Longitude, Latitude)
           
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")  # WGS84 (lat/lon) to Mercator (x/y in meters)        
    x, y = transformer.transform(lat, lon)

    min_x, min_y = transformer.transform(min_lat, min_lon)
    max_x, max_y = transformer.transform(max_lat, max_lon)
            
            # Calculate the horizontal and vertical proportions
    x_proportion = (x - min_x) / (max_x - min_x)
    y_proportion = (y - min_y) / (max_y - min_y)

            # Convert these proportions to pixel coordinates
    newx = img_width*fullSize
    mewy =img_height*fullSize
    pixel_x = int(x_proportion * newx)
    pixel_y = int((1 - y_proportion) * mewy)  # Invert y to match image coordinate system
    
    return pixel_x, pixel_y

def pixel_to_wgs84(pixel_x, pixel_y):
    # Define the bounds of the image in Mercator projection
    min_lon, max_lat = -180, 85  # Top-Left (Longitude, Latitude)
    max_lon, min_lat = 180, -85  # Bottom-Right (Longitude, Latitude)

    # Create a transformer for Mercator to WGS84
    mercator_to_wgs84 = Transformer.from_crs("epsg:3857", "epsg:4326")
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")

    # Define the image bounds in Mercator projection (meters)
    mercator_min_x, mercator_min_y = transformer.transform(min_lat, min_lon)
    mercator_max_x, mercator_max_y = transformer.transform(max_lat, max_lon)
    
    # Calculate the pixel coordinates in Mercator projection
    mercator_x = mercator_min_x + (pixel_x / (img_width * fullSize)) * (mercator_max_x - mercator_min_x)
    mercator_y = mercator_min_y + (1 - (pixel_y / (img_height * fullSize))) * (mercator_max_y - mercator_min_y)
    #print(f'mercator_x {mercator_x} and mercator_y = {mercator_y} and maxX = {mercator_max_x} and maxY = {mercator_min_y}')
    #print(f'mercator min x: `{mercator_min_x} and min y is {mercator_min_y}')
    
    lon, lat = mercator_to_wgs84.transform(mercator_x, mercator_y)
    
    return lat,lon

