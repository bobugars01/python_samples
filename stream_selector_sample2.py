builder = data_collector.get_pipeline_builder()
raw_data = json.dumps([{'name': 'Dima'}, {'name': 'Vu'}, {'name': 'Kirit'}])
dev_raw_data_source = builder.add_stage('Dev Raw Data Source')
dev_raw_data_source.set_attributes(data_format='JSON', 
                                   json_content='ARRAY_OBJECTS', 
                                   raw_data=raw_data)
stream_selector = builder.add_stage('Stream Selector')
trash_1 = builder.add_stage('Trash')
trash_2 = builder.add_stage('Trash')
dev_raw_data_source >> stream_selector >> trash_1
stream_selector >> trash_2
stream_selector.condition = [dict(outputLane=stream_selector.output_lanes[0],
                                   predicate="${record:value('/name') == 'Dima'}"),
                              dict(outputLane=stream_selector.output_lanes[1],
                                   predicate='default')]
pipeline = builder.build('Keep Dima')
data_collector.add_pipeline(pipeline)