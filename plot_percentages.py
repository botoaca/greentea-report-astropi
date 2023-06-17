# note(@botoaca): This script is used to plot the percentages of vegetation in each image from the file generated by
#                 get_vegetation_percentages.py.

import matplotlib.pyplot as plt

def main():
    with open("vegetation_percentages.txt", "r") as f:
        percentages = [l.rstrip("\n").split(": ") for l in f]
        percentages = percentages[:-2]
    percentages = [(int(p[0].split("_")[1].split(".")[0]), float(p[1])) for p in percentages]
    
    percentages.sort(key=lambda x: x[0])
    plt.bar([p[0] for p in percentages], [p[1] for p in percentages], color="lime")
    plt.xlabel("Image number")
    plt.ylabel("Percentage of vegetation")
    plt.title("Percentage of vegetation in each image")
    plt.savefig("vegetation_percentages.png", dpi=300)

if __name__ == "__main__":
    main()