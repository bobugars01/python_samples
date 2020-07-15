from streamsets.sdk import DataCollector
##connection to SDC
server_url = 'http://ip-10-80-4-223.eu-west-1.compute.internal:18630/'
data_collector = DataCollector(server_url)
builder = data_collector.get_pipeline_builder()
directory_source = builder.add_stage('Directory')
trash = builder.add_stage('Trash')
trash1 = builder.add_stage('Trash')
stream_selector = builder.add_stage('Stream Selector')
## Directory Origin
directory_source.label='JSON Input'
directory_source.files_directory='/Users/borisbugarski/Documents/data'
directory_source.file_name_pattern='*.json'
directory_source.data_format='JSON'
directory_source >> stream_selector
stream_selector >> trash
stream_selector >> trash1

##stream selector
stream_selector.condition = [{'outputLane': stream_selector.output_lanes[0],
                                          'predicate': '${record:attribute("sourceId") == "DOESNOTEXIST"}'},
                                         {'outputLane': stream_selector.output_lanes[1],
                                          'predicate': 'default'}]
pipeline = builder.build('Sample Pipeline')
data_collector.add_pipeline(pipeline)