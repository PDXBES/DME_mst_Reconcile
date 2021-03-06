from businessclasses.config import Config
from businessclasses.dme_master_hybrid import DmeMasterHybrid
from businessclasses.dme_master_link import DmeMasterLink
from dataio.dme_master_hybrid_db_data_io import DmeMasterHybridDbDataIo
import time

start = time.time()

config = Config('TEST')
dme_master_hybrid = DmeMasterHybrid(config)
dme_master_hybrid_db_data_io = DmeMasterHybridDbDataIo(config)

## will write out result for a subset of mlinks specified in CCSP.MASTER_LINK_NAMES (specified in view)
## 1. create in memory version of DME links
## 2. create in memory version of EMGAATS links which have already been subset to project area
## 3. overwrite information from EMGAATS links to DME links where global_ids match
## 4. append result to CCSP.DME_MASTER_HYBRID

start = time.time()
test_dme_pipes = dme_master_hybrid.create_dme_links(dme_master_hybrid_db_data_io)
print time.time() - start

start = time.time()
test_ccsp_master_links = dme_master_hybrid.create_ccsp_master_links(dme_master_hybrid_db_data_io)
print time.time() - start

dme_master_links = []
start = time.time()

for test_ccsp_master_link in test_ccsp_master_links:
    dme_master_link = DmeMasterLink(config)
    dme_master_link.global_id = test_ccsp_master_link.global_id
    dme_master_link.link_id = test_ccsp_master_link.link_id
    dme_master_link.us_depth = test_ccsp_master_link.us_depth
    dme_master_link.ds_depth = test_ccsp_master_link.ds_depth
    dme_master_link.us_ie = test_ccsp_master_link.us_ie
    dme_master_link.ds_ie = test_ccsp_master_link.ds_ie
    dme_master_link.us_depth_source = "Master"
    dme_master_link.ds_depth_source = "Master"
    for index, dme_link in enumerate(test_dme_pipes):
        if dme_link.global_id == test_ccsp_master_link.global_id:
            dme_master_link.compkey = dme_link.compkey
            dme_master_link.diameter = dme_link.diameter
            dme_master_link.geometry = dme_link.geometry
            dme_master_link.us_node_name = dme_link.us_node_name
            dme_master_link.ds_node_name = dme_link.ds_node_name
            dme_master_links.append(dme_master_link)
            test_dme_pipes.pop(index)
            break
print time.time() - start
start = time.time()
dme_master_hybrid_db_data_io.append_dme_master_links_to_db(dme_master_links)
print time.time() - start
pass
