
from google.cloud import vision


class handwriting_identifier:
    def __init__(self, path_to_image):
        self.image_path = 'uploads/4.jpg'

    def detect_document(self):
        client = vision.ImageAnnotatorClient()

        with open(self.image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.document_text_detection(image=image)
        found_words = []

        text_detection_config = {'language_codes': ['en']}

        features = [{'type': vision.Feature.Type.TEXT_DETECTION,
                     'text_detection.config': text_detection_config}]

        response = client.annotate_image(
            {'image': image, 'features': features})

        detected_text = response.text_annotations[0].description

        print('1')
        print(detected_text)

        # for page in response.full_text_annotation.pages:
        #     for block in page.blocks:
        #         for paragraph in block.paragraphs:
        #             paragraph_text = ''.join(
        #                 [word.symbols[0].text for word in paragraph.words])
        #             words = paragraph_text.split()
        #             for i, word in enumerate(words):
        #                 if word == 'cash' or word.lower() == 'credit':
        #                     if i < len(words) - 1 and words[i+1].isdigit():
        #                         amount = words[i+1]
        #                         found_words.append((word, amount))
        #
        # if response.error.message:
        #     raise Exception(
        #         '{}\nFor more info on error messages, check: '
        #         'https://cloud.google.com/apis/design/errors'.format(
        #             response.error.message))
        if found_words != []:
            print(found_words)
        else:
            print("No words found")

        return found_words
