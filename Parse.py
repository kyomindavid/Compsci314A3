'''
Created on 2015. 7. 13.
@author: Se-young Yu

Modified by: Kyomin Ku
'''

import datetime

class Parser:
    
    #Define variables in Java way
    def __init__(self):
        self.numberOfDays = 0 # Count number of Days passed

        self.startDate = datetime.date.today()
        self.endDate = datetime.date.today()    
        
        self.fileTypeDict = dict() # Contains file extension - file type information       
        
        self.initializeFileType()

    def getFileType(URI):
        
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'): return 'HTML'
        filename = URI.split('/')[-1]
        
        if '?' in filename: return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        else : return 'Others'
        
    def initializeFileType(self) :
        # Define file types for each file       
        
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"        

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"        

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"    
    

    # Read Each line from the log and process output    
    def parse(self, logFile):

        index = 0
        temp = ''
        totalRequests = 0
        totalBytes = 0
        countLocalClients = 0
        localClientsBytes = 0
		
        successful = 0
        found = 0
        notModified = 0
        unsuccessful = 0

        html = 0
        images = 0
        sound = 0
        video = 0
        formatted = 0
        dynamic = 0
        others = 0

        htmlB = 0
        imagesB = 0
        soundB = 0
        videoB = 0
        formattedB = 0
        dynamicB = 0
        othersB = 0

        array = []
        
        #debug = open('debug2.txt', 'w')
        for line in logFile:
               
            # Skip to the next line if this line has an empty string
            if line is None: continue
            
            elements = line.split()
            sourceAddress = elements[0]
            timeStr = elements[3].replace('[', '')
            requestMethod = elements[5].replace('"','')
            requestFileName = elements[6].replace('"','')
            
            # Skip to the next line if this line contains not equal to 9 - 11 elements
            
            if not(len(elements) == 10 or len(elements) == 9 or len(elements) == 11):
                continue
                
            #If there is more than 1 element in user information, correct the index of other elements
            timeStrIndex = 0
            for idx, val in enumerate(elements):
                if '-0600]'  == val : break 
                timeStrIndex = idx
                
            timeStr = elements[timeStrIndex].replace('[', '')
            requestMethod = elements[timeStrIndex+2].replace('"','')
            requestFileName = elements[timeStrIndex+3].replace('"','')
            self.endDate = datetime.datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")

            #If this line is the first or the last line, store date information
            if index is 0: self.startDate = self.endDate
            
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]
            
            #put HTTPversion as empty string if not exist
            if len(elements) <= 10: HTTPversion = elements[7]                
            else: HTTPversion = elements[6]
            
            if not ('HTTP' in HTTPversion or '1.0' in HTTPversion):
                HTTPversion = ""
            

            ################## From Here ##################
            # Implement your parser here to generate statistics output 
            
            index += 1
            if responseCode == '200':
                successful += 1
                if replySizeInBytes.isdigit():
                    totalBytes += int(replySizeInBytes)
                    #debug.write(str(index) + '\t' + replySizeInBytes + '\n')
                if ('usask.ca') in sourceAddress:
                    countLocalClients += 1
                    if replySizeInBytes.isdigit():
                        localClientsBytes += int(replySizeInBytes)
                elif ('128.233') in sourceAddress:
                    countLocalClients += 1
                    if replySizeInBytes.isdigit():
                        localClientsBytes += int(replySizeInBytes)
                #elif ('USASK.CA') in sourceAddress:
                    #countLocalClients += 1
                   # if replySizeInBytes.isdigit():
                      #  localClientsBytes += int(replySizeInBytes)

                for idx, val in enumerate(array):
                    if val == list:
                        break
                    else:
                        array.append(line)
                
                        
                # HTTP
                if requestFileName.endswith('/') or requestFileName.endswith('.') or requestFileName.endswith('..'):
                    html += 1
                    if replySizeInBytes.isdigit():
                        htmlB += int(replySizeInBytes)
                elif '.html' in requestFileName:
                    html += 1
                    htmlB += int(replySizeInBytes)
                elif '.htm' in requestFileName:
                    html += 1
                    htmlB += int(replySizeInBytes)
                elif '.shtml' in requestFileName:
                    html += 1
                    htmlB += int(replySizeInBytes)
                elif '.map' in requestFileName:
                    html += 1
                    htmlB += int(replySizeInBytes)
                # Images
                elif '.GIF' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.gif' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.jpeg' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.jpg' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.xbm' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.bmp' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.rgb' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                elif '.xpm' in requestFileName:
                    images += 1
                    imagesB += int(replySizeInBytes)
                # Sound
                elif '.au' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.snd' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.wav' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.mid' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.midi' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.lha' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.aif' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                elif '.aiff' in requestFileName:
                    sound += 1
                    soundB += int(replySizeInBytes)
                # Video
                elif '.mov' in requestFileName:
                    video += 1
                    videoB += int(replySizeInBytes)
                elif '.movie' in requestFileName:
                    video += 1
                    videoB += int(replySizeInBytes)
                elif '.avi' in requestFileName:
                    video += 1
                    videoB += int(replySizeInBytes)
                elif '.qt' in requestFileName:
                    video += 1
                    videoB += int(replySizeInBytes)
                elif '.mpeg' in requestFileName:
                    video += 1
                    videoB += int(replySizeInBytes)
                elif '.mpg' in requestFileName:
                    video += 1
                    videoB += int(replySizeInBytes)
                # Formatted
                elif '.ps' in requestFileName:
                    formatted += 1
                    formattedB += int(replySizeInBytes)
                elif '.eps' in requestFileName:
                    formatted += 1
                    formattedB += int(replySizeInBytes)
                elif '.doc' in requestFileName:
                    formatted += 1
                    formattedB += int(replySizeInBytes)
                elif '.dvi' in requestFileName:
                    formatted += 1
                    formattedB += int(replySizeInBytes)
                elif '.txt' in requestFileName:
                    formatted += 1
                    formattedB += int(replySizeInBytes)
                # Dynamic
                elif '?' in requestFileName:
                    dynamic += 1
                    dynamicB += int(replySizeInBytes)
                elif '.cgi' in requestFileName:
                    dynamic += 1
                    dynamicB += int(replySizeInBytes)
                elif '.pl' in requestFileName:
                    dynamic += 1
                    dynamicB += int(replySizeInBytes)
                elif '.cgi-bin' in requestFileName:
                    dynamic += 1
                    dynamicB += int(replySizeInBytes)
                else:
                    others += 1
                    if replySizeInBytes.isdigit():
                        othersB += int(replySizeInBytes)
                    

                
            elif responseCode == '302':
                found += 1
            elif responseCode == '304':
                notModified += 1
            else:
                unsuccessful += 1

			
            totalRequests += 1

        print('Total number of requests:', totalRequests)
        print('Total bytes transfered is', totalBytes)
        print('')
        print('No. of successful responses:', successful)
        print('No. of found responses:', found)
        print('No. of not modified responses :', notModified)
        print('No. of unsuccessful responses:', unsuccessful)
        print('successful + found + notModified + unsuccessful =', successful + found + notModified + unsuccessful)
        print('')
        print('No. of local clients:', countLocalClients)
        print('Local clients bytes transfered is', localClientsBytes)    
        print('')
        print('No. of Html:', html)
        print('No. of Images:', images)
        print('No. of Sound:', sound)
        print('No. of Video:', video)
        print('No. of Formatted:', formatted)
        print('No. of Dynamic:', dynamic)
        print('No. of Others:', others)
        print('')
        print('No. of Html bytes:', htmlB)
        print('No. of Images bytes:', imagesB)
        print('No. of Sound bytes:', soundB)
        print('No. of Video bytes:', videoB)
        print('No. of Formatted bytes:', formattedB)
        print('No. of Dynamic bytes:', dynamicB)
        print('No. of Others bytes:', othersB)
        print('')
        print('No. of unique object request', len(array))
        '''
            print('{0} , {1} , {2}, {3} , {4} , {5} , {6}'.
                  format(sourceAddress,timeStr,requestMethod,requestFileName,HTTPversion, responseCode, replySizeInBytes),end="")
            
            if not replySizeInBytes.isdigit(): continue;
            
            fileType = self.getFileType(requestFileName)
            print(' , {0}'.format(fileType))
        ''' 
        #debug.close()

        
    def checkResCode(self, code):
        if code == '200' : return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'   
        return None
        
if __name__ == '__main__':
    logfile = open('UofS_access_log','r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
    pass
