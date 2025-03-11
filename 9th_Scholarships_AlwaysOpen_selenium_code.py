#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas selenium webdriver-manager')
get_ipython().system('pip install openpyxl')


# In[ ]:





# In[14]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime


# In[15]:


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)


# In[16]:


base_url="https://www.buddy4study.com/open-scholarships?filter=eyJSRUxJR0lPTiI6W10sIkdFTkRFUiI6W10sIkVEVUNBVElPTiI6WyIxMCJdLCJDT1VOVFJZIjpbXSwiQ09VUlNFIjpbXSwiU1RBVEUiOltdLCJGT1JFSUdOIjpbXSwic29ydE9yZGVyIjoiREVBRExJTkUifQ=="


# In[17]:


driver.get(base_url)


# In[18]:


scholarship_links = []
while True:
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'Listing_categoriesBox')]")))
        scholarships = driver.find_elements(By.XPATH, "//a[contains(@class, 'Listing_categoriesBox')]")

        for scholarship in scholarships:
            link = scholarship.get_attribute("href")
            if link and link not in scholarship_links:
                scholarship_links.append(link)

        # Move to the next page if available
        try:
            next_page = driver.find_element(By.XPATH, f"//li[contains(@class, 'rc-pagination-item') and text()='{current_page + 1}']")
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(5)  # Allow new page to load
        except:
            print("No more pages left. Exiting pagination loop.")
            break

    except Exception as e:
        print(f"Error while extracting listing: {e}")
        break


# In[19]:


len(scholarship_links)


# In[20]:


data = {
            'URL': [],
            'Scholarship Name': [],
            'Awards': [],
            'Eligibility': [],
            'Benefits': [],
            'Deadline Date': [],
            'About Program': []
        }

def find_about_program_content(driver):
    """ Scrapes all paragraphs under class names starting with 'ScholarshipDetails_aboutProgram'. """
    try:
        paragraphs = driver.find_elements(By.XPATH, "//*[starts-with(@class, 'ScholarshipDetails_aboutProgram')]//p")
        content = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        return content if content else "N/A"
    except:
        return "N/A"

for index, scholarship_url in enumerate(scholarship_links[:400]):
    try:
        driver.get(scholarship_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        # Extract details
        data['URL'].append(scholarship_url)

        # Scholarship Name
        try:
            title = driver.find_element(By.TAG_NAME, "h1").text.strip()
            data['Scholarship Name'].append(title)
        except:
            data['Scholarship Name'].append("N/A")

        # Award Details
        try:
            award_element = driver.find_element(By.XPATH, "//*[contains(@class, 'ScholarshipDetails_studyLine')]")
            data['Awards'].append(award_element.text.strip())
        except:
            data['Awards'].append("N/A")

        # Eligibility
        try:
            eligibility_element = driver.find_element(By.XPATH, "//h5[contains(., 'Eligibility')]/following-sibling::div[contains(@class, 'ScholarshipDetails_studyLine')]")
            data['Eligibility'].append(eligibility_element.text.strip())
        except:
            data['Eligibility'].append("N/A")

        # Benefits
        try:
            benefits_element = driver.find_element(By.XPATH, "//h5[contains(., 'Benefits')]/following-sibling::div[contains(@class, 'ScholarshipDetails_studyLine')]")
            data['Benefits'].append(benefits_element.text.strip())
        except:
            data['Benefits'].append("N/A")

        # Deadline Date
        try:
            deadline_element = driver.find_element(By.XPATH, "//span[contains(@class, 'ScholarshipDetails_cardDate')]")
            data['Deadline Date'].append(deadline_element.text.replace("Deadline Date:", "").strip())
        except:
            data['Deadline Date'].append("N/A")

        # About Program
        about_program = find_about_program_content(driver)
        data['About Program'].append(about_program)

        print(f"Scraped {index+1}/{len(scholarship_links)}: {data['Scholarship Name'][-1]}")

    except Exception as e:
        print(f"Error processing {scholarship_url}: {e}")
        data['Scholarship Name'].append("N/A")
        data['Awards'].append("N/A")
        data['Eligibility'].append("N/A")
        data['Benefits'].append("N/A")
        data['Deadline Date'].append("N/A")
        data['About Program'].append("N/A")



# In[21]:


data


# In[22]:


# Save data to Excel
df = pd.DataFrame(data)
file_name = f"9th_Scholarships_All_Open_07-03-25.csv"
df.to_csv(file_name, index=False)
print(f"\nScraping completed! Data saved to {file_name}")


# In[23]:


driver.quit()


# In[ ]:





# In[ ]:





# In[ ]:




