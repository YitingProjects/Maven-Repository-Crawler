import requests
from lxml import html
from bs4 import BeautifulSoup
import csv
from MavenRepositoryCrawler.CSVCreator import CSVCreator

import time
from datetime import datetime
import wget

class MavenParser:

    def __init__(self, group_id, artifact_id):
        self.maven_page_table = None
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.gourp_id_url = 'https://mvnrepository.com/artifact/' + self.group_id + '/'
        self.artifact_id_url = 'https://mvnrepository.com/artifact/' + self.group_id + '/' + self.artifact_id + '/'

        self._load_page()

    def _load_page(self):
        """
        Use BeautifulSoup4 lib to scrape information in the table from the artifact page
        :return:
        """


        r = requests.get(self.artifact_id_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        web_table = soup.find('table', class_='grid versions')
        tbodies = web_table.find_all('tbody')

        # reverse the table content to get information from old to new
        self.maven_page_table = list(reversed(tbodies))




    def get_artifact_version_list(self):

        output = []

        for tbody in self.maven_page_table:

            if len(tbody.td['rowspan']) == 0:
                elements = tbody('td')

            elif len(tbody.td['rowspan']) == 1:
                elements = tbody('td')[1:]
            else:
                print('Error: the format of table is not matched.')
                return


            version_inf_array = reversed([elements[x:x + 4] for x in range(0, len(elements), 4)]) # transform the content to 2 dimension array


            """
            transform the information array into json list
            """
            for element in version_inf_array:

                # v : version, r : repository type, c : clients, d : release date
                version = element[0]
                repository_type = element[1]
                client_inf = element[2]
                release_date = element[3]


                version_inf = {
                    'version' : {'v_number': version.get_text(),
                                 'url': version('a')[0]['href']
                                 },
                    'repository_type' : repository_type.get_text(),
                    'client_inf':{'count': client_inf.get_text(),
                                  'url': client_inf('a')[0]['href']
                                  },
                    'release_date': release_date.get_text()
                }

                output.append(version_inf)

        return output


    def save_artifact_inf_to_csv(self, output_file_name, row_span=False):

        header = ['version-v_number', 'version-url', 'repository_type', 'client_inf-count', 'client_inf-url', 'release_date']
        csvCreater = CSVCreator(output_file_name)
        csvCreater.add_header(header)

        output_data = []
        for tbody in self.maven_page_table:

            if len(tbody.td['rowspan']) == 0:
                elements = tbody('td')

            elif len(tbody.td['rowspan']) == 1:
                elements = tbody('td')[1:]
            else:
                print('Error: the format of table is not matched.')
                return


            version_inf_array = reversed([elements[x:x + 4] for x in range(0, len(elements), 4)]) # transform the content to 2 dimension array


            """
            transform the information array into json list
            """
            for element in version_inf_array:

                # v : version, r : repository type, c : clients, d : release date
                version = element[0]
                repository_type = element[1]
                client_inf = element[2]
                release_date = element[3]

                version_inf = (version.get_text(), version('a')[0]['href'], repository_type.get_text(), client_inf.get_text(),
                               client_inf('a')[0]['href'], release_date.get_text())

                output_data.append(version_inf)

        csvCreater.save_data(output_data)


