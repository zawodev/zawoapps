import numpy as np

class Captcha:
    def __init__(self, image_path, missing_piece_size=(20, 20), canvas_size=(96, 64)):
        self.image_path = image_path
        self.missing_piece_size = missing_piece_size
        self.canvas_size = canvas_size
        self.axis = 'x'  # default axis
        self.offset = [0, 0]  # [x, y] offsets for missing piece
        self.original_position = None
        self.base_image, self.missing_piece, self.masked_image = self._prepare_images()

    def _prepare_images(self):
        # load the input image
        image = cv2.imread(self.image_path)
        image = cv2.resize(image, self.canvas_size)  # resize to fit the canvas
    
        # create the missing piece
        x, y = np.random.randint(0, self.canvas_size[0] - self.missing_piece_size[0]), np.random.randint(0, self.canvas_size[1] - self.missing_piece_size[1])
        self.original_position = (x, y)
        piece = image[y:y + self.missing_piece_size[1], x:x + self.missing_piece_size[0]].copy()
    
        # create a masked version of the image
        masked_image = image.copy()
        masked_image[y:y + self.missing_piece_size[1], x:x + self.missing_piece_size[0]] = 0  # make the piece black
    
        # add white border around the black square
        masked_image[y:y + self.missing_piece_size[1], x] = 255  # left border
        masked_image[y:y + self.missing_piece_size[1], x + self.missing_piece_size[0] - 1] = 255  # right border
        masked_image[y, x:x + self.missing_piece_size[0]] = 255  # top border
        masked_image[y + self.missing_piece_size[1] - 1, x:x + self.missing_piece_size[0]] = 255  # bottom border
    
        return image, piece, masked_image

    def translate_piece(self, delta):
        if self.axis == 'x':
            self.offset[0] = max(0, min(self.offset[0] + delta, self.canvas_size[0] - self.missing_piece_size[0] - 4))
        elif self.axis == 'y':
            self.offset[1] = max(0, min(self.offset[1] + delta, self.canvas_size[1] - self.missing_piece_size[1] - 4))

    def switch_axis(self):
        self.axis = 'y' if self.axis == 'x' else 'x'

    def confirm_position(self):
        # check if the piece is placed close enough to the original position
        tolerance = 2  # allowable margin of error in pixels
        original_x, original_y = self.original_position
        
        #print(f"original_x: {original_x}, original_y: {original_y}")
        #print(f"offset_x: {self.offset[0]}, offset_y: {self.offset[1]}")

        if abs(original_x - self.offset[0] - 2) <= tolerance and abs(original_y - self.offset[1] - 2) <= tolerance:
            return True
        return False

    def get_combined_image(self):
        # combine the masked image and the piece with the current offset
        combined_image = self.masked_image.copy()
        x, y = self.offset
        # draw the piece with a border
        piece_with_border = self._add_border_to_piece()
        piece_h, piece_w = piece_with_border.shape[:2]
        combined_image[y:y + piece_h, x:x + piece_w] = piece_with_border
        return combined_image

    def _add_border_to_piece(self):
        # add a black and white border to the missing piece
        piece_with_border = cv2.copyMakeBorder(
            self.missing_piece, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 255, 255]
        )
        piece_with_border = cv2.copyMakeBorder(
            piece_with_border, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 0]
        )
        return piece_with_border

    def save_for_display(self):
        # save the combined image for displaying on the SSD1331
        combined_image = self.get_combined_image()
        cv2.imwrite("display_image.png", combined_image)

if __name__ == "__main__":
    import cv2

    captcha = Captcha("cat.png")

    def handle_key(event):
        if event == ord('q'):
            if captcha.confirm_position():
                print("Captcha solved correctly!")
            else:
                print("Captcha failed!")
        elif event == ord('e'):
            captcha.switch_axis()
            print(f"Switched to {captcha.axis} axis.")
        elif event == ord('a'):  # left arrow
            captcha.translate_piece(-1)
        elif event == ord('d'):  # right arrow
            captcha.translate_piece(1)

        # show the current combined image
        combined_image = captcha.get_combined_image()
        cv2.imshow("Captcha", combined_image)

    cv2.imshow("Captcha", captcha.get_combined_image())

    while True:
        key = cv2.waitKey(0)
        if key == 27:  # escape key
            break
        handle_key(key)

    cv2.destroyAllWindows()
