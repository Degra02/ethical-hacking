from PIL import Image, ImageChops

im1 = Image.open("./flag.png")
im2 = Image.open("./peppers.png")

res = ImageChops.logical_xor(im1, im2)
res.save('sol.png')
