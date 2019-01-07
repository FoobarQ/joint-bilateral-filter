import cv2, math, sys, easygui

# applies the gaussian functions give the pixel locations & colour values
def weight(x, y, eye1, eye2, sigma_space, sigma_intensity):
    return math.exp((-(x**2+y**2)/(sigma_space**2)) - ((max(eye1, eye2)-min(eye1, eye2))**2/(sigma_intensity**2)))

# calculates the euclidean distance between colour values
def calculate_intensity_difference(p1, p2):
    p1 = list(map(int, p1))
    p2 = list(map(int, p2))
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)


def joint_bilateral(image, image2, filter_size, sigma_intensity, sigma_space):
    # is used to create the relative filter positions
    filter_range = filter_size//2
    # stores the relative positions
    filter_matrix = []
    # creates a matrix filled with zeros the same dimensions of the original image
    output_image = image.copy()
    # populates the filter_matrix
    for i in range(-filter_range, filter_range+1):
        for j in range(-filter_range, filter_range+1):
            filter_matrix.append([i, j])

    for i in range(len(image)):
        for j in range(len(image[i])):
            neighbourhood_total = [0, 0, 0]
            normalisation_total = [0, 0, 0]

            for k in filter_matrix:
                if i + k[0] < 0 or j + k[1] < 0 or j + k[1] >= image.shape[1] or i + k[0] >= image.shape[0]:
                    # kernel cropping is applied if this condition is satisfied.
                    pass
                else:
                    intensity_difference = calculate_intensity_difference(image2[i, j], image2[i+k[0], j+k[1]])
                    individual_weight = weight(k[0], k[1], intensity_difference*2, intensity_difference, sigma_space,
                                               sigma_intensity)
                    for n in range(3):
                        neighbourhood_total[n] += individual_weight * image[i+k[0], j+k[1], n]
                        normalisation_total[n] += individual_weight

            for n in range(3):
                output_image[i, j, n] = (neighbourhood_total[n] // normalisation_total[n]) 

    output_image = cv2.cvtColor(output_image, cv2.COLOR_LAB2BGR)

    return output_image


def main():
    if len(sys.argv) == 3:
        img = cv2.imread(sys.argv[1])
        img2 = cv2.imread(sys.argv[2])
    else:
        img = cv2.imread(easygui.fileopenbox())
        img2 = cv2.imread(easygui.fileopenbox)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)

    s_i = float(input("sigma intensity: "))
    s_s = float(input("sigma space: "))
    filter_size = int(input("neighbourhood size: "))
    
    if s_s < 0 and filter_size > 0:   #if s_s is < 0, it'll be given a value based off of the filter and the opencv implementation
        s_s = 0.3*((filter_size-1)*0.5 - 1) + 0.8
    else:
        filter_size = int((((s_s - 0.8)/0.3) + 1)*2 + 1)
    
    joint_bilateral(img, img2, filter_size, s_i, s_s)



if __name__ == '__main__':
    main()
