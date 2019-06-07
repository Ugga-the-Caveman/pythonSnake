from imports import BrainClass


length = int(input("Enter snake length: "))
if length < 1:
    exit("length < 1")

width = int(input("Enter world width: "))
if width < 1:
    exit("width < 1")

height = int(input("Enter world height: "))
if height < 1:
    exit("height < 1")

print(f"Brain with {width * height} inputs initialized.")
thisBrain = BrainClass(width, height, length)


print("Enter a positive Nr. of Nodes to add a layer. Enter 0 to stop adding layers.")
layerCount = 1
ble = int(input(f"layer {layerCount}: "))

while ble > 0:
    thisBrain.addLayer(ble)
    layerCount += 1
    ble = int(input(f"layer {layerCount}: "))


if len(thisBrain.lyrs) == 0 or len(thisBrain.lyrs[-1]) != 4:
    thisBrain.addLayer(4)
    print("Output layer should have 4 Nodes. Output layer added.")


thisBrain.randomize()


print("Enter filename to save this Brain.")
ble = False
while not ble:
    filename = input("Enter filename: ")
    ble = thisBrain.save(filename)
