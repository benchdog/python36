/* File         : error.go
 * Author       : liqingbo
 * Date         : 2016-03-25 10:16:02
 * Last modified: 2016-03-25 10:16:02
 */
package common

const (
	ERROR_CODE_NO_ERROR = 0
)

const (
	ERROR_CODE_NO_PERMISSION = 4

	ERROR_CODE_PARAM_ERROR   = 31023
	ERROR_CODE_NETWORK_ERROR = 31021 // majiazhi 20180105

	ERROR_PCS_REFUSE = 31034

	//account error, from 41 to 60
	ERROR_ACCOUNT_NOT_AUTHORIZE = 31044
	ERROR_ACCOUNT_NO_USER       = 31045
	ERROR_ACCOUNT_PASS_RELOGIN  = 31047

	//file error, from 61 to 80
	ERROR_FILE_NOT_AUTHORIZE   = 31064
	ERROR_FILE_NOT_EXIST       = 31066
	ERROR_FILE_GET_META_FAILED = 31071
	ERROR_DIR_NOT_DOWNLOAD     = 31074

	ERROR_BLOOD_SUCKING      = 31326
	ERROR_HOTLINK_FORBIDDEN  = 31426
	ERROR_HOTLINK_RAND_ERROR = 31526
	ERROR_EXPIRE_TIMEOUT     = 31360

	ERROR_SIGN_ERROR                  = 31362
	ERROR_ILLEGAL_FILE_ERROR          = 31390
	ERROR_ILLEGAL_FILE_ERROR_FOR_PCTB = 31396

	ERROR_PCS_INTERNAL_ERROR = 31035
	// add
	//ERROR_NO_URLS             = 39000
)

var errorMsg = map[int]string{
	ERROR_CODE_NO_ERROR: "success",

	ERROR_CODE_NO_PERMISSION: "No permission to do this operation",

	//
	ERROR_CODE_PARAM_ERROR:      "param error",
	ERROR_PCS_REFUSE:            "pcs refuse service",
	ERROR_CODE_NETWORK_ERROR:    "network error", // majiazhi 20180105
	ERROR_ACCOUNT_NOT_AUTHORIZE: "user is not authorized",
	ERROR_ACCOUNT_NO_USER:       "user not exists",
	ERROR_ACCOUNT_PASS_RELOGIN:  "user must relogin",

	ERROR_FILE_NOT_AUTHORIZE:   "file is not authorized",
	ERROR_FILE_NOT_EXIST:       "file does not exist",
	ERROR_FILE_GET_META_FAILED: "get file meta failed",
	ERROR_DIR_NOT_DOWNLOAD:     "directory can't be downloaded",

	ERROR_BLOOD_SUCKING:      "anti hotlinking",
	ERROR_HOTLINK_FORBIDDEN:  "hotlinking forbidden",
	ERROR_HOTLINK_RAND_ERROR: "rand error",
	ERROR_EXPIRE_TIMEOUT:     "expire time out error",

	ERROR_SIGN_ERROR:                  "sign error",
	ERROR_ILLEGAL_FILE_ERROR:          "Illegal File",
	ERROR_ILLEGAL_FILE_ERROR_FOR_PCTB: "Illegal File  for Pc Tongbu",

	ERROR_PCS_INTERNAL_ERROR: "pcs internal error",

	//ERROR_NO_URLS:             "no urls",
}

var errorHttpStatus = map[int]int{

	ERROR_CODE_NO_PERMISSION: 403,

	ERROR_CODE_PARAM_ERROR:   400,
	ERROR_CODE_NETWORK_ERROR: 403, // majiazhi 20180108

	ERROR_PCS_REFUSE: 400,

	ERROR_ACCOUNT_NOT_AUTHORIZE: 403,
	ERROR_ACCOUNT_NO_USER:       403,
	ERROR_ACCOUNT_PASS_RELOGIN:  403,

	ERROR_FILE_NOT_AUTHORIZE:   403,
	ERROR_FILE_NOT_EXIST:       404,
	ERROR_FILE_GET_META_FAILED: 503,
	ERROR_DIR_NOT_DOWNLOAD:     403,

	ERROR_BLOOD_SUCKING:      403,
	ERROR_HOTLINK_FORBIDDEN:  403,
	ERROR_HOTLINK_RAND_ERROR: 403,
	ERROR_EXPIRE_TIMEOUT:     403,

	ERROR_SIGN_ERROR:                  403,
	ERROR_ILLEGAL_FILE_ERROR:          403,
	ERROR_ILLEGAL_FILE_ERROR_FOR_PCTB: 404,

	ERROR_PCS_INTERNAL_ERROR: 503,

	//ERROR_NO_URLS:             404,
}

func ErrorMsg(code int) string {
	return errorMsg[code]
}

func ErrorHttpStatus(code int) int {
	return errorHttpStatus[code]
}

type ResponceBody struct {
	ErrorCode int    `json:"error_code"`
	ErrorMsg  string `json:"error_msg"`
}

type ResBodyError struct {
	ErrorCode int    `json:"error_code"`
	ErrorMsg  string `json:"error_msg"`
	ErrorInfo string `json:"error_info"`
	RequestId int64  `json:"request_id"`
}

type ResBodyErrorWithRedo struct {
	Redo      int    `json:"redo"`
	ErrorCode int    `json:"error_code"`
	ErrorMsg  string `json:"error_msg"`
	ErrorInfo string `json:"error_info"`
	RequestId int64  `json:"request_id"`
}
