from flask import session
import csv

class ImageController:
    """Controller for managing image sequences in the speech practice."""
    file_path = 'app/static/datas/flashcard.csv'

    # Tạo map để lưu dữ liệu
    data_map = {}

    # Mở file với encoding UTF-8 (phù hợp với tiếng Nhật)
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        
        # Nếu có header thì bỏ qua dòng đầu
        next(reader, None)
        
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                data_map[key] = value

    IMAGE_LIST = list(data_map.keys())

    # # In ra kết quả kiểm tra
    # for k, v in data_map.items():
    #     print(f"{k} : {v}")

    # # List of image filenames in static/imgs directory
    # IMAGE_LIST = ['1.png', '2.png', '3.png']  # Add your image filenames here
    
    @classmethod
    def get_current_image(self):
        """Get the current image filename."""
        # Initialize image index in session if not exists
        if 'current_image_index' not in session:
            session['current_image_index'] = 0
            
        return self.IMAGE_LIST[session['current_image_index']]
    
    @classmethod
    def get_next_image(self):
        """Get the next image filename and update session."""
        if 'current_image_index' not in session:
            session['current_image_index'] = 0
        else:
            # Increment index and wrap around if at end
            session['current_image_index'] = (session['current_image_index'] + 1) % len(self.IMAGE_LIST)
            
        return self.IMAGE_LIST[session['current_image_index']]

    @classmethod
    def get_current_text(self):
        """Get the current text of image."""
        # Initialize image index in session if not exists
        if 'current_image_index' not in session:
            session['current_image_index'] = 0

        return self.data_map[self.IMAGE_LIST[session['current_image_index']]]
