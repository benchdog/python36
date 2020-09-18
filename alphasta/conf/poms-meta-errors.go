// Go MySQL Driver - A MySQL-Driver for Go's database/sql package
//
// Copyright 2013 The Go-MySQL-Driver Authors. All rights reserved.
//
// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this file,
// You can obtain one at http://mozilla.org/MPL/2.0/.

package utils

import (
	"fmt"
)

type PomsmetaError struct {
	Status int
	Errno  int
	ErrMsg string
}

func (e *PomsmetaError) Error() string {
	return fmt.Sprintf("{\"error_code\":%d,\"error_msg\":\"%s\"}", e.Errno, e.ErrMsg)
}

/*
* TODO: Various errors poms meta might return. Can change between driver versions.
* -  errors classification        |  error_code
*  - meta error                   |
*  - param invalid/missing        |
*  - result invalid/missing       |
*  - data service error           |
*  - network error                |
*  - cache error                  |
*  - data error                   |
*  - inner conf error             |
*  - mcpack error                 |
 */

var (
	Success = PomsmetaError{200, 0, ""}

	//meta error
	ErrApiUnsupport            = PomsmetaError{400, -12000, "Unsupported api"}
	ErrApiPathUnsupport        = PomsmetaError{400, -12001, "Unsupported path. It should begin with '/rest/2.0/poms/'"}
	ErrDropInnerExpiredRequest = PomsmetaError{500, -12003, "Drop inner expired request"}

	//param invalid/missing
	ErrInvalidHttpRequest              = PomsmetaError{400, -12100, "Invalid http request"}
	ErrParamInvalidPomsKey             = PomsmetaError{400, -12101, "Invalid param poms key"}
	ErrParamInvalidPartKey             = PomsmetaError{400, -12103, "Invalid param part key"}
	ErrParamInvalidRange               = PomsmetaError{400, -12102, "Invalid param range"}
	ErrParamInvalidMD5                 = PomsmetaError{400, -12548, "Invalid param md5"}
	ErrParamInvalidSize                = PomsmetaError{400, -12554, "Invalid param size"}
	ErrParamInvalidCRC32               = PomsmetaError{400, -12553, "Invalid param crc32"}
	ErrParamInvalidUploadID            = PomsmetaError{404, -12466, "List superfile2 failed: invalid upload_id"}
	ErrParamFirstRegionAndRangeUnmatch = PomsmetaError{400, -12107, "Param info-first-region and range unmatch"}
	ErrParamSizeUnconsistentDDBSSize   = PomsmetaError{400, -12579, "Input param size unconsistent with the output size from DDBS"}
	ErrParamInvalidBucket              = PomsmetaError{400, -12200, "Invalid param bucket"}
	ErrParamInvalidObject              = PomsmetaError{400, -12201, "Invalid param object"}
	ErrInvalidPomsMetaType             = PomsmetaError{400, -12202, "Poms meta type invalid"}
	ErrCheckerMetaTableIsMissing       = PomsmetaError{503, -12203, "Checker meta table conf missing"}
	ErrBcsBucketLengthInvalid          = PomsmetaError{400, -12204, "Bucket name length invalid"}
	ErrBcsObjectLengthInvalid          = PomsmetaError{400, -12205, "Object name length invalid"}
	ErInvalidrVersionKey               = PomsmetaError{400, -12206, "Version key invalid"}
	ErrBcsObjectShouldBeginWithSlash   = PomsmetaError{400, -12207, "Object name should begin with slash"}
	ErrPomsKeyType1ObjectType          = PomsmetaError{404, -12208, "There is no type 1 poms key for specified object type"}
	ErrPomsKeyType2ObjectType          = PomsmetaError{404, -12209, "There is no type 1 poms key for specified object type"}
	ErrUnSupportedType                 = PomsmetaError{400, -12210, "Object type unsupported"}
	ErrUnSupportedExpectedIDC          = PomsmetaError{404, -12470, "Unsupported expected-data-idc"}
	ErrInvalidInputParam               = PomsmetaError{400, -12602, "Invalid input param"}
	ErrInvalidRange                    = PomsmetaError{416, -12477, "Invalid range"}
	ErrCheckSuperfileKeylistInvalid    = PomsmetaError{503, -12211, "Check superfile's keylist invalid"}
	ErrCheckSuperfile2KeylistInvalid   = PomsmetaError{503, -12213, "Check superfile2's keylist invalid"}
	// - insert api
	ErrParamInvalidUniqueKey        = PomsmetaError{400, -12214, "Invalid param unique_key"}
	ErrParamInvalidCdateTime        = PomsmetaError{400, -12215, "Invalid param cdatetime"}
	ErrParamInvalidSliceKeyProtocol = PomsmetaError{400, -12216, "Invalid param slice_key_protocol"}
	ErrParamInvalidClusterId        = PomsmetaError{400, -12217, "Invalid param cluster_id"}
	ErrParamInvalidTableName        = PomsmetaError{400, -12218, "Invalid param table_name"}
	ErrParamObjectTypeMissing       = PomsmetaError{400, -12219, "Missing object type param"}
	ErrParamInvalidKeyList          = PomsmetaError{400, -12237, "Invalid param keylist"}
	//different from ErrParamInvalidUploadID
	ErrParamUploadIDInvalid = PomsmetaError{400, -12220, "Invalid param upload_id"}
	ErrParamInvalidPartID   = PomsmetaError{400, -12221, "Invalid param part_id"}
	// - insertsuperfile2part
	ErrUploadFirstSuperfile2PartLessThan4MB         = PomsmetaError{400, -12222, "Size of superfile2 first part should not be smaller than 4MB"}
	ErrInsertSuperfile2PartAbortedCommitedOrDeleted = PomsmetaError{404, -12223, "Insert superfile2 part: superfile2 aborted, commited or deleted"}
	ErrInsertSuperfile2PartUploadIDNotExisting      = PomsmetaError{503, -12224, "Insert superfile2 part: upload_id is not existing in DDBS"}
	// - commitsuperfile2
	ErrCommitSuperfile2PartNumNoLessThan2 = PomsmetaError{400, -12225, "Commit superfile2 failed: part num should not be smaller than 2"}
	ErrCommitSuperfile2InvalidPartList    = PomsmetaError{400, -12226, "Commit superfile2 invalid part list"}
	ErrParamInvalidUploadKey              = PomsmetaError{400, -12227, "Invalid param upload_key"}
	ErrParamInvalidXService             = PomsmetaError{400, -12299, "Invalid param x-service"}
	ErrParamInvalidStatus                 = PomsmetaError{400, -12228, "Invalid param status"}
	ErrParamInvalidFrom                   = PomsmetaError{400, -12229, "Invalid param from"}
	ErrParamInvalidTo                     = PomsmetaError{400, -12230, "Invalid param to"}
	ErrParamInvalidTag                    = PomsmetaError{400, -12231, "Invalid param tag"}
	ErrParamInvalidAppCode                = PomsmetaError{400, -12232, "Invalid param app_code"}
	ErrParamInvalidResponse               = PomsmetaError{400, -12233, "Invalid param response"}
	ErrParamInvalidSeq                    = PomsmetaError{400, -12234, "Invalid param seq"}
	ErrParamInvalidMetaList               = PomsmetaError{400, -12233, "Invalid param meta_list"}
	ErrParamInvalidUID                    = PomsmetaError{400, -12234, "Invalid param uid"}
	ErrParamInvalidIsFastPut              = PomsmetaError{400, -12235, "Invalid param is_fastput"}
	ErrParamInvalidSourceKey              = PomsmetaError{400, -12236, "Invalid param source key"}

	/* inner error */
	//result invalid/missing
	ErrOneObjectSuperfileMetaNotExistingInDDBS = PomsmetaError{503, -12474, "Meta of the only sub object is not existing in DDBS"}
	ErrObjectDeprecatedDataClusterId           = PomsmetaError{400, -12400, "Deprecated data cluster"}
	ErrNoAvaliableKeyListDistribution          = PomsmetaError{503, -12527, "No avaliable key_list_distribution"}
	ErrBcsQueryRegionFailed                    = PomsmetaError{404, -12343, "Query bucket region failed"}
	ErrPomsKeyNotExistingInDDBS                = PomsmetaError{404, -12003, "Poms key is not existing in DDBS"}
	ErrUploadIDotExistingInDDBS                = PomsmetaError{404, -12479, "Upload_id is not existing in ddbs"}
	ErrObjectIsNotExisting                     = PomsmetaError{404, -12010, "Object is not existing"}
	ErrGetClusterIdByAnalyzeResultFailed       = PomsmetaError{503, -12401, "Get cluster_id based on analyze_result failed"}
	ErrSuperfileSubObjectNotExistingInDDBS     = PomsmetaError{503, -12402, "Meta of the sub object is not existing in DDBS"}
	ErrSuperfile2SubPartNotExistingInDDBS      = PomsmetaError{503, -12403, "Meta of the sub part is not existing in DDBS"}
	ErrDataJsonDecodeFailed                    = PomsmetaError{400, -12404, "Upload info need to formated as an array"}
	ErrBuildUploadInfoFailed                   = PomsmetaError{503, -12405, "Build analyze_result from upload info failed"}
	// - commitsuperfile2
	ErrCommitSuperfile2NotInited              = PomsmetaError{404, -12406, "Commit superfile2: superfile2 is not inited"}
	ErrCommitSuperfile2UploadConflict         = PomsmetaError{404, -12407, "Commit superfile2 failed: upload_id conflict"}
	ErrCommitSuperfile2NotCommited            = PomsmetaError{404, -12408, "Commit superfile2 failed: superfile2 is not uncommited"}
	ErrCommitSuperfile2PartNotExistingInDDBS  = PomsmetaError{404, -12409, "Commit superfile2 failed: some parts are not existing in DDBS"}
	ErrCommitSuperfile2PartIDNotMatched       = PomsmetaError{400, -12410, "Commit superfile2 failed: part_id and part_key not matched"}
	ErrCommitSuperfile2LastPartSizeNotBeZero  = PomsmetaError{404, -12411, "Commit superfile2 failed: size of last part should not be 0"}
	ErrCommitSuperfile2PartSizeNotLessThan4MB = PomsmetaError{404, -12412, "Commit superfile2 failed: size of part(except last one) should not be smaller than 4MB"}
	ErrCommitSuperfile2UpdateStatusFailed     = PomsmetaError{503, -12413, "Commit superfile2 failed: update superfile2 status in DDBS failed"}
	ErrUpdateDDBSFailed                       = PomsmetaError{503, -12414, "Update DDBS failed"}
	ErrUpdatePomsKeyHasManyRecords            = PomsmetaError{503, -12415, "Update DDBS failed : poms_key has many records"}
	// commitsuperfile3
	ErrParamInvalidUniqueKeyDsitribution = PomsmetaError{400, -12499, "Invalid param unique_key_distribution"}
	//superobject
	ErrCommitSuperObjectNotInited                = PomsmetaError{404, -12416, "Commit superobject failed: superobject is not uncommited"}
	ErrCommitSuperObjectUploadConflict           = PomsmetaError{503, -12417, "Commit superobject failed: upload_id conflict"}
	ErrCommitSuperObjectNotCommited              = PomsmetaError{404, -12418, "Commit superobject failed: superobject is not uncommited"}
	ErrCommitSuperObjectUpdateStatusFailed       = PomsmetaError{503, -12419, "Commit superobject failed: update superobject status in DDBS failed"}
	ErrCommitSuperObjectInsertMD5TableFailed     = PomsmetaError{503, -12420, "Commit superobject failed: insert superobject into md5 table failed"}
	ErrBuildMetaFromDBFailed                     = PomsmetaError{503, -12421, "Build analyze_result from DDBS failed"}
	ErrExplodePomsKeyFailed                      = PomsmetaError{503, -12422, "Explode poms_key failed"}
	ErrUploadKeyConflict                         = PomsmetaError{400, -12423, "Conflicted with upload_key"}
	ErrInsertSuperfile2PartTempNotExistingInDDBS = PomsmetaError{404, -12424, "Insert superfile2 temp failed:  parts are not existing in DDBS"}
	ErrInsertSuperfile2PartTempUploadIDReUsed    = PomsmetaError{400, -12425, "Commit one part superfile2_temp failed: uplaod_id has already used"}
	ErrCheckSuperfile2PartTempFailed             = PomsmetaError{400, -12426, "Commit one part superfile2_temp failed: check superfile2 part temp failed"}
	ErrSuperfile2PartTempUploadIdConflict        = PomsmetaError{400, -12427, "Commit one part superfile2_temp failed: upload_id conflict"}
	ErrUpdateDDBSParamInvalid                    = PomsmetaError{400, -12428, "Update DDBS param invalid"}
	ErrSuperfile3UploadIdConflict                = PomsmetaError{500, -12428, "Commit superfile3 failed: upload_id conflict"}
	ErrCommitSuperfile3NotInited                 = PomsmetaError{404, -12406, "Commit superfile3: superfile3 is not inited"}
	ErrCommitSuperfile3UpdateStatusFailed        = PomsmetaError{503, -12413, "Commit superfile3 failed: update superfile2 status in DDBS failed"}

	//database service error
	ErrDBConnectFailed                         = PomsmetaError{503, -12201, "DB connect failed"}
	ErrDBQueryFailed                           = PomsmetaError{503, -12202, "DB query failed"}
	ErrDBInsertFailed                          = PomsmetaError{503, -12203, "DB insert failed"}
	ErrDBInsertConflictWithUniqueKey           = PomsmetaError{400, -12204, "Insert normal object conflict in unique key"}
	ErrDBUpdatePomsMetaFailed                  = PomsmetaError{503, -12205, "Update poms meta table failed"}
	ErrDBQuerySuperfile2PartNotExisting        = PomsmetaError{404, -12206, "Superfile2 part not existing in ddbs"}
	ErrDBExecuteFailed                         = PomsmetaError{503, -12207, "DB sql execute failed"}
	ErrInsertSuperfile2PartConflictWithPartKey = PomsmetaError{400, -12208, "Insert superfile2 part failed: part_key conflict"}
	ErrUpdateMD5CRC32Conflict                  = PomsmetaError{503, -12209, "Update md5/crc32 failed: md5/crc32 conflict with DDBS"}

	//network error
	ErrNetworkCheckGetKeyFailed         = PomsmetaError{503, -12301, "Check and get key failed"}
	ErrNetworkAccessFailed              = PomsmetaError{503, -12302, "Network access failed"}
	ErrHttpQueryFailed                  = PomsmetaError{503, -12327, "Select meta from mola failed"}
	ErrHttpQueryFromKeyListInsertFailed = PomsmetaError{503, -12328, "Select meta from KeylistInsert API failed"}
	ErrGenPomsDataUrlFailed             = PomsmetaError{503, -12603, "Generate poms-data url failed"}
	ErrGetOptimalMetaFailed             = PomsmetaError{503, -12604, "Get Optimal Meta failed"}
	ErrSearchRefKeyNotFound             = PomsmetaError{503, -12605, "Ref_key not found in mola"}
	ErrSearchKeyFailed                  = PomsmetaError{503, -12606, "Search key from mola failed"}
	ErrSearchKeysInMetaTableFailed      = PomsmetaError{503, -12607, "Search keys in all meta table failed"}

	//cache service error
	ErrCacheConnectFailed        = PomsmetaError{503, -12401, "Cache connect failed"}
	ErrCacheQueryFailed          = PomsmetaError{503, -12402, "Cache Query failed"}
	ErrPomsCacheInvalidTableName = PomsmetaError{503, -12403, "Cache table name invalid"}
	ErrPomsCacheSetStringFailed  = PomsmetaError{503, -12405, "Cache set string failed"}
	ErrPomsCacheGetStringFailed  = PomsmetaError{503, -12405, "Cache get string failed"}
	ErrSQLCacheParamInvalid      = PomsmetaError{400, -12406, "SQL Cache param invalid"}
	ErrSQLCacheEncodeFailed      = PomsmetaError{500, -12407, "SQL Cache encode invalid"}
	ErrResponseEncodeFailed      = PomsmetaError{500, -12408, "Response json encode failed"}
	ErrPomsCacheHGetFailed       = PomsmetaError{503, -12409, "Cache hget string failed"}
	ErrPomsCacheGetBitFailed     = PomsmetaError{503, -12410, "Cache getbit string failed"}
	ErrPomsCacheSetFailed        = PomsmetaError{503, -12411, "Cache set string failed"}

	//data error
	ErrUnpackBcsMetaFailed                     = PomsmetaError{503, -12500, "Unpack bcs meta failed"}
	ErrContentLengthMissingFromBcsMeta         = PomsmetaError{503, -12501, "CONTENT_LENGTH missing from meta"}
	ErrQueryPomsDataKeyNotFound                = PomsmetaError{404, -12502, "Select meta from mola not found"}
	ErrPomsKeyRelevantDataHasAlreadyCorrupted  = PomsmetaError{404, -12573, "Poms key relevant data has arleady corrupted"}
	ErrPomsKeyRelevantDataHasAlreadyDeleted    = PomsmetaError{404, -12574, "Poms key relevant data has already deleted"}
	ErrPomsKeyRelevantDataHasAlreadyMd5deduped = PomsmetaError{404, -12575, "Poms key relevant data has already md5deduped and no available data"}
	ErrCheckPomsKeyStatusImpossible            = PomsmetaError{400, -12576, "Check poms key status in DDBS: impossible"}
	ErrPomsKeyIsNotExisting                    = PomsmetaError{404, -12577, "Poms_key is not existing"}
	ErrUFCNotInited                            = PomsmetaError{500, -12578, "Ufc service not inited"}
	ErrDecodeServiceResponseFailed             = PomsmetaError{500, -12579, "Decode service response failed"}

	//inner conf error
	ErrCheckerAreaConfMissing      = PomsmetaError{503, -12600, "Checker area conf missing"}
	ErrPomsDomainConfMissing       = PomsmetaError{503, -12601, "Poms domain conf missing"}
	ErrPomsKeyStatusMappingMissing = PomsmetaError{503, -12605, "Poms key status mapping missing"}
	ErrMultiSearchMapIndexInvalid  = PomsmetaError{500, -12606, "Multi search keys map index invalid"}
	ErrRepairRefMetaFailed         = PomsmetaError{503, -12607, "Repair ref_meta failed"}

	//Mcpack
	ErrMcpackCheckContentLengthIsMissing        = PomsmetaError{503, -12380, "Check mcpack Content-Length missing"}
	ErrMcpackCheckCreateTimeIsMissing           = PomsmetaError{503, -12381, "Check mcpack create_time missing"}
	ErrMcpackCheckCVersionIsMissing             = PomsmetaError{503, -12382, "Check mcpack version missing"}
	ErrMcpackCheckRefKeyIsMissing               = PomsmetaError{503, -12383, "Check mcpack ref_key missing"}
	ErrMcpackCheckUrlIsMissing                  = PomsmetaError{503, -12384, "Check mcpack url missing"}
	ErrMcpackCheckCommitedIsMissing             = PomsmetaError{503, -12385, "Check mcpack commited missing"}
	ErrMcpackCheckPartListIsMissing             = PomsmetaError{503, -12386, "Check mcpack part_list missing"}
	ErrMcpackCheckPartListSizeIsMissing         = PomsmetaError{503, -12387, "Check mcpack part_list size missing"}
	ErrMcpackCheckSubObjectMetaClusterIsMissing = PomsmetaError{503, -12388, "Check mcpack subobject_meta_cluster size missing"}
	ErrMcpackCheckSliceListIsMissing            = PomsmetaError{503, -12389, "Check mcpack slice_list size missing"}
	ErrMcpackCheckClusterIdIsMissing            = PomsmetaError{503, -12390, "Check mcpack cluster_id missing"}
	ErrMcpackCheckTableNameIsMissing            = PomsmetaError{503, -12391, "Check mcpack table_name missing"}
	ErrMcpackCheckEtagIsMissing                 = PomsmetaError{503, -12392, "Check mcpack Etag missing"}
	ErrMcpackCheckMetaListMetaCRC32IsMissing    = PomsmetaError{503, -12393, "Check mcpack meta_list x-bs-meta-crc32 missing"}
	ErrMcpackCheckUploadIdIsMissing             = PomsmetaError{503, -12394, "Check mcpack upload_id missing"}
	ErrMcpackCheckUniqueKeyDistributionMissing  = PomsmetaError{503, -12395, "Check mcpack unique_key_distribution missing"}
	ErrMcpackCheckBucketNameFailed              = PomsmetaError{503, -12396, "Check mcpack bucket name failed"}
	ErrMcpackNewSliceKeyProtocolMolaMetaEmpty   = PomsmetaError{503, -12397, "Select ref key of new slice key protocol normal object success in mola, but meta is empty"}
	ErrMcpackInsertSuperfileMissingSubObject    = PomsmetaError{503, -12398, "Multi select superfile check sub-object miss key"}
	ErrQueryBcsMetaTable                        = PomsmetaError{503, -12399, "Query bcs meta table failed"}
	ErrQuerySuperfileSubObjectNewProtcolFailed  = PomsmetaError{503, -12400, "Superfile sub object is using new slice_key_protocol but meta is empty"}
	ErrMultiSelectFromMolaNotFound              = PomsmetaError{503, -12401, "Multi select from mola result not found"}
	ErrCheckAnalyzeResultExisting               = PomsmetaError{503, -12402, "Check analyze_result existing failed"}
	ErrCheckSmallObjectUnsupported              = PomsmetaError{400, -12403, "Meta basic check: Small object is unsupported"}

	//asyncui:12300-12350
	ErrSendAsyncUIFailed               = PomsmetaError{503, -12300, "Send msg to asyncui failed"}
	ErrAsyncuiNonblockingParamInvalid  = PomsmetaError{400, -12301, "Asyncui param non-blocking invalid"}
	ErrAsyncuiPostDataJsonEncodeFailed = PomsmetaError{500, -12302, "Asyncui post data feild json encode failed"}
	ErrAsyncuiUFCInitFailed            = PomsmetaError{500, -12303, "Asyncui init ufc request failed"}
	ErrAtaskProcessingJsonEncodeFailed = PomsmetaError{500, -12304, "Asyncui atask processing json encode failed"}
	ErrAtaskProcessingJsonDecodeFailed = PomsmetaError{500, -12305, "Asyncui atask processing json decode failed"}
	ErrAtaskCacheJsonEncodeFailed      = PomsmetaError{500, -12306, "Asyncui atask cache json encode failed"}
	ErrAtaskCacheJsonDecodeFailed      = PomsmetaError{500, -12307, "Asyncui atask cache json decode failed"}
	ErrGetAtaskProcessingFailed        = PomsmetaError{500, -12308, "Asyncui atask processing get failed"}
	ErrSetAtaskProcessingFailed        = PomsmetaError{500, -12309, "Asyncui atask processing set failed"}
	ErrGetAtaskCacheFailed             = PomsmetaError{500, -12310, "Asyncui atask cache get failed"}
	ErrSetAtaskCacheFailed             = PomsmetaError{500, -12311, "Asyncui atask cache set failed"}
	ErrAtaskNotExisted                 = PomsmetaError{400, -12312, "Asyncui atask not existed"}
	ErrHistoryTableNameInvalid         = PomsmetaError{500, -12313, "Event history table_name invalid"}
	ErrInsertIntoHistoryParamInvalid   = PomsmetaError{500, -12314, "Insert event history param invalid"}
	ErrDelAtaskCacheFailed             = PomsmetaError{500, -12315, "Asyncui atask cache del failed"}

	//atask:12350-
	ErrMD5computeOnlyTye1v1Supported    = PomsmetaError{400, -12350, "Atask md5compute only support type1v1 poms_key"}
	ErrMD5computeStatusNotSupported     = PomsmetaError{400, -12351, "Atask md5compute poms_key's status not supported"}
	ErrMD5computeTypeNotSupported       = PomsmetaError{400, -12352, "Atask md5compute poms_key's type not supported"}
	ErrMD5computeMD5AlreadyExisted      = PomsmetaError{400, -12353, "Atask md5compute poms_key's md5 already existed"}
	ErrMD5computeGetPomsKeyIDCFailed    = PomsmetaError{503, -12354, "Atask md5compute get poms_key's distribution idc failed"}
	ErrAtaskParamActionNotMatched       = PomsmetaError{503, -12355, "Atask param action not match"}
	ErrMD5ComputeMD5OrCRC32UnConsistent = PomsmetaError{503, -12356, "Atask md5compute crc32/md5 unconsistent"}
	ErrAtaskParamMissing                = PomsmetaError{503, -12357, "Atask param missing"}
	ErrSuperObjInitFailed               = PomsmetaError{503, -12358, "Atask init superobject failed"}
	ErrKeyListDistributionInvalid       = PomsmetaError{503, -12359, "Atask flow keylistdistribution invalid"}
	ErrUniqueKeyListDistributionInvalid = PomsmetaError{503, -12360, "Atask flow uniquekeydistribution invalid"}
	ErrFlowGetSrcIdcFailed              = PomsmetaError{404, -12361, "Atask flow get srcidc failed"}
	ErrFlowS2FormatInvalid              = PomsmetaError{503, -12362, "Atask flow s2 format invalid"}
	ErrFlowKeylistdistruteFormatInvalid = PomsmetaError{503, -12363, "Atask flow s2 keylistdistribution format invalid"}
	ErrFlowUKListDistributionInvalid    = PomsmetaError{503, -12364, "Atask flow s2 uniquekeydistribution format invalid"}
	ErrFlowSendDelayQueueFail           = PomsmetaError{503, -12365, "Atask flow send delayqueue msg failed"}
	ErrCleanType2v2NotSupported         = PomsmetaError{400, -12366, "Atask clean not support type2v2 poms_key"}
	ErrCleanStatusNotSupported          = PomsmetaError{400, -12367, "Atask clean status not supported"}
	ErrCleanTypeNotSupported            = PomsmetaError{400, -12368, "Atask clean type not supported"}
	ErrCleanStatusUnconsisted           = PomsmetaError{400, -12369, "Atask Clean unmatched record or status"}
	ErrCleanKeyListDistributionInvalid  = PomsmetaError{500, -12370, "Atask Clean superfile2 part key_list_distribution invalid"}
	ErrCleanCacheQueryFailed            = PomsmetaError{400, -12371, "Atask Clean atask cache query failed"}
	ErrCleanMultiStatusUnconsisted      = PomsmetaError{400, -12372, "Atask Clean multi records unmatched record or status"}
	ErrCleanCallbackFailed              = PomsmetaError{200, -12373, "Atask Cleancallback done: response=-1"}
	ErrCleanDedupNoMD5                  = PomsmetaError{500, -12374, "Atask Clean dedup poms_key no md5"}
	ErrCleanDedupNoAvaliableObject      = PomsmetaError{500, -12375, "Atask Clean dedup poms_key has no status=0 object"}

	//degrade
	ErrLoadExceedSystemCapability   = PomsmetaError{406, -12700, "degrade because load exceed system capablity"}
	ErrDBLoadExceedSystemCapability = PomsmetaError{406, -12701, "degrade because database load exceed capablity"}
	ErrHittingSQLBlackList          = PomsmetaError{406, -12702, "degrade because request hit sql blacklist"}
	ErrForbidURIDegraded            = PomsmetaError{406, -12703, "degrade because request hit forbid uri"}
	ErrResourceManageDegraded       = PomsmetaError{406, -12704, "degrade because resource manage sdk forbid"}

	//redis error
	ErrCacheTryLockHasLocked = PomsmetaError{406, -12800, "Too much Meta insert into ddbs concurrence"}

	//special error_code
	ErrHittingUnrefDeletedMeta     = PomsmetaError{404, -12900, "Object is not existing"}
	ErrHittingUnrefDDBSDeletedMeta = PomsmetaError{404, -12901, "Object is not existing"}

	//blocklist error
	ErrOneLineRecord        = PomsmetaError{400, -15001, "Invalid PomsMeta Dump Record"}
	ErrBlockListJsonDecode  = PomsmetaError{400, -15002, "Invalid PomsMeta KeyList Decode"}
	ErrMD5Incorrect         = PomsmetaError{400, -15003, "One subject MD5 Should Same the superfile"}
	ErrKeyRairInRedisFailed = PomsmetaError{400, -15004, "Key Repair In NDB Failed"}
	ErrKeyValueUnexpect     = PomsmetaError{400, -15005, "Key Value Get From Redis Unexpect"}
	ErrConvertStr2IntFailed = PomsmetaError{400, -15006, "Convert string to int failed"}
	ErrBlockListWrongFormat = PomsmetaError{503, -15007, "Blocklist cache invalid format"}

	//unknowr error
	ErrUnknown = PomsmetaError{400, -12999, "Unknown error"}
)
