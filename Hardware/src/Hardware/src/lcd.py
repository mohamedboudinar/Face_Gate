import lcd_driver
from PIL import Image, ImageDraw, ImageFont, ImageColor

class LcdProcess:
    def __init__(self) -> None:
        self.disp = lcd_driver.LCD()
        Lcd_ScanDir = lcd_driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
        self.disp.LCD_Init(Lcd_ScanDir)
        self.disp.LCD_Clear()

    def create_image_with_text_main(self, selected=None):
        # Create a new image with a black background
        image = Image.new('RGB', (self.disp.width, self.disp.height), color='black')

        # Initialize ImageDraw
        draw = ImageDraw.Draw(image)

        # Define the text and font
        texts = ["Check in", "Check out", "Pause"]
        font = ImageFont.load_default()  # Load default font

        # Calculate positions
        width, height = image.size
        text_height = draw.textbbox((0, 0), texts[2], font=font)[3]
        positions = [0, height // 2, height - text_height]

        # Draw the texts on the image
        for i, text in enumerate(texts):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = positions[i]

            if text == selected:
                # Highlight the selected text
                draw.rectangle([x-10, y-10, x+text_width+10, y+text_height+10], outline="white")

            draw.text((x, y), text, font=font, fill='white')

        return image

    # Function to show "Checked in" message
    def create_image_with_text(self, text_in):
        # Create a new image with a black background
        image = Image.new('RGB', (self.disp.width, self.disp.height), color='black')

        # Initialize ImageDraw
        draw = ImageDraw.Draw(image)

        # Define the text and font
        text = text_in
        font = ImageFont.load_default()  # Load default font

        # Calculate position
        width, height = image.size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw the text on the image
        draw.text((x, y), text, font=font, fill='white')

        return image

    def show_main_menu(self):
        frame = self.create_image_with_text_main()
        self.disp.LCD_ShowImage(frame, 0, 0)

    def show_check_in_menu(self):
        frame = self.create_image_with_text('Checked in')
        self.disp.LCD_ShowImage(frame, 0, 0)

    def show_out_menu(self):
        frame = self.create_image_with_text('Checked out')
        self.disp.LCD_ShowImage(frame, 0, 0)

    def show_rejected_menu(self):
        frame = self.create_image_with_text('Rejected!')
        self.disp.LCD_ShowImage(frame, 0, 0)

    def check_button_check_in(self):
        return self.disp.digital_read(self.disp.GPIO_KEY1_PIN)

    def check_button_check_out(self):
        return self.disp.digital_read(self.disp.GPIO_KEY3_PIN)

if __name__ == '__main__':
    lcd = LcdProcess()
    lcd.show_rejected_menu()

