from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os


class MangaScraper:
    def __init__(self):
        pass

    def replace_space(self, name):
        return name.replace(" ", "-")
    def replace_space_to_plus(self,name):
         return name.replace(" ", "+")

    def scrape_data(self, name, chapter):
        url = "https://3asq.org/manga/" + self.replace_space(name) + "/" + str(chapter) + "/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        images = soup.find_all('img')
        image_list = []

        if len(images) == 0:
            return {
                "status": 404,
                "error": "Chapter not found",
                "message": "The chapter you are looking for is not available"
            }

        for image in images:
            image_url = image['src'].strip('\t\n')
            image_list.append(image_url)

        return {
            "status": 200,
            "message": "The chapter manga is available",
            "data": image_list
        }
    
    def download_chapter(self, name, chapter):
        result = self.scrape_data(name, chapter)

        if result['status'] != 200:
            return result

        image_list = result['data']

        # Download the images
        local_images = []
        for i, image_url in enumerate(image_list):
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            file_name = f"{name}_chapter_{chapter}_{i}.png"
            img.save(file_name)  # Save image locally
            local_images.append(file_name)

        # Create a PDF from the downloaded images
        pdf_file_name = f"{name}_chapter_{chapter}.pdf"
        self.create_pdf(local_images, pdf_file_name)
        self.delete_pdf_images(local_images)

        return {
            "status": 200,
            "message": f"Chapter {chapter} of {name} downloaded and saved as {pdf_file_name}",
            "pdf_file": pdf_file_name
        }
    def search_for_manga(self, name):
        url = "https://3asq.org/?s=" + self.replace_space_to_plus(name) + "&post_type=wp-manga"
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        manga_entries = soup.select('.tab-content-wrap .c-tabs-item__content')
        manga_list = []

        for entry in manga_entries:
            title_element = entry.select_one('h3.h4 a')
            image_element = entry.select_one('.c-image-hover a img')

            if title_element and image_element:
                title = title_element.get_text(strip=True)
                image_src = image_element['src'] if 'src' in image_element.attrs else None
                
                manga_list.append({
                    "title": title,
                    "image_src": image_src
                })

        if len(manga_list) == 0:
            return {
                "status": 404,
                "error": "no manga found",
                "message": "The manga you are looking for is not available"
            }

        return {
            "status": 200,
            "message": "The manga is available",
            "data": manga_list
        }
        
    def create_pdf(self, image_files, output_pdf):
        images = []

        for image_file in image_files:
            img = Image.open(image_file)
            img = img.convert("RGB")  # Convert to RGB mode required for PDF
            images.append(img)

        if images:
            # Save all images as a single PDF
            images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF created: {output_pdf} 📄")
    # Delete the images after creating the PDF
    def delete_pdf_images(self, image_files):
        for image_file in image_files:
            os.remove(image_file)
    # Download a range of chapters
    def download_manga_from_to(self, name, start, end):
        for chapter in range(start, end + 1):
            result = self.download_chapter(name, chapter)
            if result['status'] != 200:
                return result

        return {
            "status": 200,
            "message": f"Chapters {start} to {end} of {name} downloaded and saved as PDFs"
        }
    