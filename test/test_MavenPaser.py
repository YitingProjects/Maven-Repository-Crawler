import unittest
import os

from MavenRepositoryCrawler.MavenParser import MavenParser

class MavenPaserTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_fl_version_list_to_csv(self):
        group_id = "junit"
        artifact_id = "junit"

        self.mp = MavenParser(group_id, artifact_id)
        output = self.mp.get_artifact_version_list()
        print(output)
        self.assertNotEqual(len(output), 0)

    def test_save_artifact_inf_to_csv(self):
        group_id = "junit"
        artifact_id = "junit"

        self.mp = MavenParser(group_id, artifact_id)
        self.mp.save_artifact_inf_to_csv("file.csv")

        self.assertGreater(os.stat('file.csv').st_size , 1800 )
        os.remove("file.csv")


#mp.get_fl_inf_to_csv(outputFLVersionList, row_span=True)  # FL version Information


#mp.downloadJars(from_version, "C:/jar2", last_version=last_version, row_span=True)






if __name__ == '__main__':

    unittest.main(verbosity=2)


