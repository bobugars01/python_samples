from streamsets.sdk import DataCollector
##connection to SDC
server_url = '<url>'
data_collector = DataCollector(server_url)
builder = data_collector.get_pipeline_builder()
directory_source = builder.add_stage('Directory')
trash = builder.add_stage('Trash')
stream_selector = builder.add_stage('Stream Selector')
local_fs1=builder.add_stage('Local FS')
local_fs1.directory_template='/Users/<user>/output'
local_fs1.data_format='JSON'
## Directory Origin
directory_source.label='JSON Input'
directory_source.files_directory='/Users/<user>/Documents/data'
directory_source.file_name_pattern='*.json'
directory_source.data_format='JSON'
directory_source >> stream_selector
stream_selector >> trash
stream_selector >> local_fs1

##stream selector
stream_selector.condition = [{'outputLane': stream_selector.output_lanes[0],
                                          'predicate': '${record:value(\'/ambient_temperature\')<\'20\'}'},
                                         {'outputLane': stream_selector.output_lanes[1],
                                          'predicate': 'default'}]
pipeline = builder.build('Sample Pipeline')
data_collector.add_pipeline(pipeline)