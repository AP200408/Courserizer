import requests
from bs4 import BeautifulSoup
import re

class CourseScraper:
  def __init__(self, url, file_name):
    self.url = url
    self.name = file_name
    self.file_path = f"./files/{file_name}.txt"
    
  def is_url_valid(self):
    try:
      response = requests.head(self.url)
      return response.status_code == 200
    except requests.RequestException:
      return False

  def scrape_course_info(self, ):
    if not self.is_url_valid():
      return ("Invalid URL")
    
    response = requests.get(self.url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='ud-heading-xl clp-lead__title clp-lead__title--small').get_text()

    by = soup.find('a', class_='ud-btn ud-btn-large ud-btn-link ud-heading-md ud-text-sm ud-instructor-links').find('span')

    rating_container = soup.find('span', class_="star-rating-module--star-wrapper--i1cJH star-rating-module--medium--Lpe62")
    rating = rating_container.find('span', class_="ud-sr-only")

    number_ratings_container = soup.find('a', class_ = "ud-btn ud-btn-large ud-btn-link ud-heading-md ud-text-sm styles--rating-wrapper--YkK4n")
    spans_without_class = number_ratings_container.select('span:not([class])')

    student_number_container = soup.find('div', class_ = 'enrollment')

    last_updated_container = soup.find('div', class_ = 'last-update-date').find('span')
    last_updated_text_content = last_updated_container.get_text().replace("Last updated", "")

    overview = soup.find('div', class_= 'ud-text-md clp-lead__headline')

    description = soup.find_all('span', class_='what-you-will-learn--objective-item--VZFww')

    free_course_description = soup.find_all('div', class_ = 'objective--objective-item--0gf07')

    course_content_titles = soup.find_all('div', class_='ud-block-list-item-content')

    who_for = soup.find('ul', class_='styles--audience__list----YbP')

    exactly_learn = soup.find_all('div', class_='show-more-module--content--Rw-xr show-more-module--with-gradient--f4HoJ')
    exactly_learn_div = exactly_learn[0]
    first_div_inside_exactly_learn = exactly_learn_div.find('div')
    second_div = first_div_inside_exactly_learn.find('div')
    first_ul_inside_first_div = second_div.find_all('ul')

    li_list = []
    for ul in first_ul_inside_first_div:
      li = ul.find_all('li')
      li_list.append(li)
        
    extracted_texts = []
    for snippet in li_list:
      for li_element in snippet:
        p_element = li_element.find('p')
        if p_element:
          p_text = p_element.get_text().strip()
          if p_text.endswith(';'):
            p_text = p_text[:-1]
          extracted_texts.append(p_text)
                  
    second_div_empty = []
    for div in first_div_inside_exactly_learn.find_all('div'):
      second_div_empty.append(div)

    p_tag = exactly_learn_div.find_all('p')
    p_tags_without_strong = [p_element for p_element in exactly_learn_div.find_all('p') if not p_element.find('strong')]


    with open(self.file_path, 'w') as file:

      #Title
      file.write("Title: " + title + '\n')
          
      # Made By
      file.write('Created by: ' + by.get_text())
          
      # Ratings and Number of Total Students
      file.write(rating.get_text()+ spans_without_class[0].get_text() + " " + student_number_container.get_text() +'\n\n')
          
      # Course Last Updated
      file.write('Course Last Updated:' + last_updated_text_content+'\n\n') 
          
      # Course Overview
      file.write('Course Overview: ' + overview.get_text()+'\n\n')

      # Paid Course
      if description:
        if extracted_texts:
          file.write("Description(General Idea): " + '\n')
        else:
          file.write("Description: " + '\n')
        desc_text = "\n".join(des.get_text() for des in description)
        file.write(desc_text.strip() + '\n\n')
            
      # Free Course
      elif free_course_description:
        if exactly_learn:
          file.write("Description(General Idea): " + '\n')
        else:
          file.write("Description: " + '\n')
        for div in free_course_description:
          sp = div.find('span')
          file.write(sp.get_text() + '\n')
      else:
        file.write("Description: " + '\n')
        file.write("No Description Provided" + '\n')
          
      # In-Depth Description
      if exactly_learn and extracted_texts:
        file.write("Description(In-Depth): " + '\n')
        if extracted_texts:
          for ele in extracted_texts:
            file.write(ele + '\n')
        else:
          if p_tags_without_strong:
            for p in p_tags_without_strong:
              file.write(p.get_text() + '\n')
                
      # Pre-requisites
      file.write('\n' + "Pre-requisites: " + '\n')
      content_text = "\n".join(div.text.strip().replace('Course', '') for div in course_content_titles if not div.find('span') and div.text.strip() not in ["Udemy Business", "Get the app", "Invite friends", "Help"] and not re.search(r'\b\d+\.\d+\s+Instructor\s+Rating\b|\b\d+\s+Reviews\b|\b\d+\s+Students\b|\b\d+\s+Courses\b|\b\d+\s+Course\b', div.text.strip()))
      file.write(content_text.strip() + '\n\n')

      # Who for?
      file.write("Who This Course Is For: " + '\n')
      if who_for:
        for li in who_for.children:
          file.write(li.get_text() + '\n')
          
  def return_text_file(self):
        try:
            with open(self.file_path, 'rb') as file:
                files = {'file': (self.file_name, file, 'text/plain')}
                response = requests.post('YOUR_BACKEND_ENDPOINT', files=files)
                if response.status_code == 200:
                    return "Text file successfully returned to the backend."
                else:
                    return "Failed to return text file to the backend."
        except FileNotFoundError:
            return "File not found."