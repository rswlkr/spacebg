import json
import os
import urllib2
from PIL import Image, ImageOps

apodUrl = 'https://api.nasa.gov/planetary/apod?api_key=JDn9Yk3fwuUBMeq4Mrn9b2RFdli8JM49HQoPDGN6'
screenResolution = [1920, 1080]

response = urllib2.urlopen(apodUrl)
data = json.load(response)

imgUrl = data["hdurl"]

image = urllib2.urlopen(imgUrl)
output = open('image.jpg', "wb")
output.write(image.read())
output.close()

bg = Image.new('RGB', screenResolution)
astroImg = Image.open('image.jpg')

originalWidth, originalHeight = astroImg.size
scale = (originalWidth / float(originalHeight))

newHeight = 800
newWidth = int(newHeight * scale)

astroImg = astroImg.resize([newWidth, newHeight])
astroImg = ImageOps.expand(astroImg, border=2, fill='white')

# move astroimg to center horizontally and to upper vertical
translateX = (screenResolution[0] - newWidth) / 2
translateY = (screenResolution[1] - newHeight) / 4
bottomOfAstroImg = translateY + newHeight
bg.paste(astroImg, [translateX, translateY])

# font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf", 15)
#
# location = (80, 0)
# text_color = (100, 100, 200)
#
# lines = textwrap.wrap("What's happening above that volcano? Although Mount Etna is seen erupting, the clouds are not related to the eruption. They are lenticular clouds formed when moist air is forced upwards near a mountain or volcano. The surreal scene was captured by chance late last month when the astrophotographer went to Mount Etna, a UNESCO World Heritage Site in Sicily, Italy, to photograph the conjunction between the Moon and the star Aldebaran. The Moon appears in a bright crescent phase, illuminating an edge of the lower lenticular cloud. Red hot lava flows on the right. Besides some breathtaking stills, a companion time-lapse video of the scene shows the lenticular clouds forming and wavering as stars trail far in the distance.", width=250)
#
# d = ImageDraw.Draw(bg)
# y_text=bottomOfAstroImg
# iteration =0
# for line in lines:
#     y_text = y_text + 18
#     d.text((30,y_text),line, font=font, fill=text_color)


bg.save("image_text.jpg")

scriptDir = os.path.dirname(os.path.realpath(__file__))
bashCommand = "gsettings set org.gnome.desktop.background picture-uri file://" + scriptDir + "/image_text.jpg"
print(bashCommand)
import subprocess

process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
