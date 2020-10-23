import unittest
import report_listing_info
import pandas as pd
from os import path
class Tect_Report_listing_info(unittest.TestCase):
 
    def test_Lisitng_in_suburb(self):
        # Test cases with valid  suburb and dates
        #format of dates are checked with format function before passing to (listings in function), so no need to test with inccorectly enterd dates
        result  = report_listing_info.listings_in_suburb("Sydney", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result) > 0)        #if results are empty
        self.assertIsInstance(result, list) #return type must be a list
        self.assertTrue(NotEmpty)           #listings with the suburbs given are in the csv gile, therefore results cannot be empty
        
        result1  = report_listing_info.listings_in_suburb("Bondi", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result1) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result1, list)

        result2  = report_listing_info.listings_in_suburb("Bondi Beach", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result2) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result2, list)

        result3  = report_listing_info.listings_in_suburb("Pyrmont", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result3) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result3, list)
        
        result4  = report_listing_info.listings_in_suburb("Manly", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result4) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result4, list)
        
        result5  = report_listing_info.listings_in_suburb("Manly,Sydney", '2020/1/1','2020/1/12',1) #can take multiple suburbs
        NotEmpty = (len(result4) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result5, list)
        self.assertTrue((len(result5) > len(result4) and len(result5) > len(result))) #combining two or more suburbs in a search 
                                                                                        #returns more listings than eithr one them indivdually


        #test that each element in the returned list is a pandas.series containing the data and has returned 96 rows for one listing       
        for i in range(len(result)):
            self.assertIsInstance(result[i], pd.Series)
            self.assertEqual(len(result[i]), 96)

        for i in range(len(result1)):
            self.assertIsInstance(result1[i], pd.Series)
            self.assertEqual(len(result1[i]), 96)

        for i in range(len(result2)):
            self.assertIsInstance(result2[i], pd.Series)
            self.assertEqual(len(result2[i]), 96)

        for i in range(len(result3)):
            self.assertIsInstance(result3[i], pd.Series)
            self.assertEqual(len(result3[i]), 96)

        for i in range(len(result4)):
            self.assertIsInstance(result4[i], pd.Series)
            self.assertEqual(len(result4[i]), 96)
        for i in range(len(result5)):
            self.assertIsInstance(result5[i], pd.Series)
            self.assertEqual(len(result5[i]), 96)

        result5  = report_listing_info.listings_in_suburb("Sydnsey", '2020/1/1','2020/1/12',1)    #invalid suburbs must return empty list
 
        self.assertEqual(len(result5),0)

        result7  = report_listing_info.listings_in_suburb("Bondi Beach", '','',1) #empty dates must return listings in surburb no matter of start and end date
        NotEmpty = (len(result7) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result7, list)
        
        result8  = report_listing_info.listings_in_suburb("", '2020/1/1','2020/1/12',1) #empty subrub will return listings only between those dates
        NotEmpty = (len(result8) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result8, list)

        result9  = report_listing_info.listings_in_suburb("", '','',1)#empty suburb and dates will return all lisitngs
        self.assertTrue(NotEmpty)
        self.assertEqual(len(result9), 500) #must return 500 lisitngs because fucntion only searches 500 at a time
        self.assertIsInstance(result9, list)

    def test_Format(self):
        #correct cases  yyyy/mm/dd
        result = report_listing_info.format(['2022','03','22'])
        self.assertTrue(result)
        result = report_listing_info.format(['2019','1','1'])
        self.assertTrue(result)
        result = report_listing_info.format(['2020','04','05'])
        self.assertTrue(result)
        result = report_listing_info.format(['2020','4','5'])
        self.assertTrue(result)
        result = report_listing_info.format(['2020','4','20'])
        self.assertTrue(result)

        #incorrect cases
        result = report_listing_info.format(['2020','29','20'])
        self.assertFalse(result)
        result = report_listing_info.format(['11','11','2018'])  
        self.assertFalse(result)     
        result = report_listing_info.format(['2016 22 22'])
        self.assertFalse(result)
        result = report_listing_info.format(['22 22','2019'])
        self.assertFalse(result)
        result = report_listing_info.format(['1d','22','2019'])
        self.assertFalse(result)
        result = report_listing_info.format(['2019','ff','2019'])
        self.assertFalse(result)
        result = report_listing_info.format(['10 Jun 2018'])
        self.assertFalse(result)
        result = report_listing_info.format(['22 Sep 2018'])
        self.assertFalse(result) 
        result = report_listing_info.format(['2222 ','10', '18','10'])
        self.assertFalse(result) 
    def test_compareDate(self): #compares if start date is greater than endd date
            #correct cases are where they are in correct formate and end date in greater than start date and in format yyyy/mm/dd
            result = report_listing_info.compare_date('2019/3/12','2019/3/10')
            self.assertTrue(result)
            result = report_listing_info.compare_date('2012/10/1','2012/9/15')
            self.assertTrue(result)
            result = report_listing_info.compare_date('2015/4/29','2015/4/28')
            self.assertTrue(result)

            #incorrect test cases
            result = report_listing_info.compare_date('2019/3/12','2019/3/18') #start date is greater, incorrect
            self.assertFalse(result)
            result = report_listing_info.compare_date('2012/15/1','2012/20/15') # month mm is greater than 12
            self.assertFalse(result)
            result = report_listing_info.compare_date('2015/4/29','2015/4/34') # day is greater than 31
            self.assertFalse(result)
            result = report_listing_info.compare_date('2019/jun/12','2019/jun/10') #has letters
            self.assertFalse(result)
            result = report_listing_info.compare_date('2012/10/1','2012/10/1')#on same day
            self.assertFalse(result)
            result = report_listing_info.compare_date('2015/4/29',float("Nan")) # date is nan this happens when a date in a listing cell is empty
            self.assertFalse(result)
            result = report_listing_info.compare_date('20112/10/1','2012/10/1')#too many digits for year
            self.assertFalse(result)
            result = report_listing_info.compare_date('2012/102/1','2012/10/11')#too many digits for month
            self.assertFalse(result)
            result = report_listing_info.compare_date('2012/10/111','2012/10/121')#too many digits for day
            self.assertFalse(result)
            result = report_listing_info.compare_date('2012/10/111/11','2012/10/121')#too many digits
            self.assertFalse(result)


    def test_Keyword(self):
              # Test cases with valid  keyword and dates
            #format of dates are checked with format function before passing to (keyword), so no need to test with inccorectly enterd dates
        result  = report_listing_info.keyword("Pool", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result) > 0)        #if results are empty
        self.assertIsInstance(result, list) #return type must be a list
        self.assertTrue(NotEmpty)           #listings with the keyword(s) given are comfirmed to be in some of the listings,
                                            # therefore results cannot be empty
        
        result1  = report_listing_info.keyword("Pet", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result1) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result1, list)

        result2  = report_listing_info.keyword("Kitchen", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result2) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result2, list)

        result3  = report_listing_info.keyword("Parking", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result3) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result3, list)
        
        result4  = report_listing_info.keyword("wifi", '2020/1/1','2020/1/12',1)
        NotEmpty = (len(result4) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result4, list)

                
        result5  = report_listing_info.keyword("wifi,pool,kitchen", '2020/1/1','2020/1/12',1) #can take multiple keywords
        NotEmpty = (len(result5) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result5, list)
        

        #test that each element in the returned list is a pandas.series containing the data and has returned 96 rows for one listing 
      
        for i in range(len(result)):
            self.assertIsInstance(result[i], pd.Series)
            self.assertEqual(len(result[i]), 96)

        for i in range(len(result1)):
            self.assertIsInstance(result1[i], pd.Series)
            self.assertEqual(len(result1[i]), 96)

        for i in range(len(result2)):
            self.assertIsInstance(result2[i], pd.Series)
            self.assertEqual(len(result2[i]), 96)

        for i in range(len(result3)):
            self.assertIsInstance(result3[i], pd.Series)
            self.assertEqual(len(result3[i]), 96)

        for i in range(len(result4)):
            self.assertIsInstance(result4[i], pd.Series)
            self.assertEqual(len(result4[i]), 96)
        for i in range(len(result5)):
            self.assertIsInstance(result5[i], pd.Series)
            self.assertEqual(len(result5[i]), 96)

  
        result6  = report_listing_info.keyword("Pooool", '2020/1/1','2020/1/12',1)       #invalid keywords must return empty list
        self.assertEqual(len(result6),0)



        result7  = report_listing_info.keyword("Pool", '','',1) #empy dates must return listings with the keyword no matter of start and end date
        NotEmpty = (len(result7) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result7, list)
        
        result8  = report_listing_info.keyword("", '2020/1/1','2020/1/12',1) #empty keyword will return all listings only between those dates
        NotEmpty = (len(result8) > 0)
        self.assertTrue(NotEmpty)
        self.assertIsInstance(result8, list)

        result9  = report_listing_info.keyword("", '','',1)#empty keyword and dates will return all lisitngs
        self.assertTrue(NotEmpty)
        self.assertEqual(len(result9), 600) #must return 600 lisitngs because fucntion only searches 500 at a time
        self.assertIsInstance(result9, list)

        result10  = report_listing_info.keyword("wifi,pool,kitchenF", '2020/1/1','2020/1/12',1) #one invalid keyword will return empty list
        Empty = (len(result10) == 0)
        self.assertTrue(Empty)
        self.assertIsInstance(result10, list)
    
    def test_comments(self):
        #function that analyses number of customers that commented on clealiness
        result = report_listing_info.comments() #function returns where the image plot was save e.g.  ...documents/data/clealiness.jpg
        #calling this function may take some time
        self.assertTrue(path.exists(result)) #true if image was saved at the path
    def test_Price_distribution(self):
         #function returns where the image plot was save e.g.  ...documents/data/clealiness.jpg
        result = report_listing_info.price_distribution('Manly','2019/4/12','2019/4/17','ManlyPrices')
        self.assertTrue(path.exists(result)) #true if image was saved at the path
        #view image to confirm name of file dates and suburb

        result = report_listing_info.price_distribution('Bondi Beach','2020/8/12','2020/8/17','BondiBeachPrices')
        self.assertTrue(path.exists(result)) #true if image was saved at the path

        result = report_listing_info.price_distribution('New York','2020/8/12','2020/8/17','New York') #if suburb does not exist
        self.assertEqual(result, -1) #true if image was saved at the path
    


        #if no suburb is given, price distrbution for all  of sydney is plotted
        result = report_listing_info.price_distribution('','2019/4/12','2019/4/17','sydneyPrices') 
        self.assertTrue(path.exists(result)) #true if image was saved at the path                
    


        #if no date if given, plot will include all prices of lisitngs regardless dates
        result = report_listing_info.price_distribution('Manly','','','ManlyPrices1') 
        self.assertTrue(path.exists(result)) #true if image was saved at the path    
        
if __name__ == "__main__":
    unittest.main()