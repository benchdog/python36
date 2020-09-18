package pcserr

import ()

type Error interface {
	HttpStatus() int
	ErrorCode() int
	ErrorMsg() string
	IsNoError() bool
	IsError(pcsError) bool
}

type pcsError int

func (e pcsError) HttpStatus() int {
	return errorHttpStatus[e]
}

func (e pcsError) ErrorCode() int {
	return int(e)
}

func (e pcsError) IsNoError() bool {
	if e == NO_ERROR {
		return true
	}
	return false
}

func (e pcsError) IsError(e2 pcsError) bool {
	if e == e2 {
		return true
	}
	return false
}

func (e pcsError) ErrorMsg() string {
	return errorMsg[e]
}

type mError struct {
	e   pcsError
	msg string
}

func (e *mError) HttpStatus() int {
	status := errorHttpStatus[e.e]
	if status == 0 {
		return errorHttpStatus[NO_ERROR]
	}
	return status
}

func (e *mError) ErrorCode() int {
	return int(e.e)
}

func (e *mError) IsNoError() bool {
	if e.e == NO_ERROR {
		return true
	}
	return false
}

func (e *mError) IsError(e2 pcsError) bool {
	if e.e == e2 {
		return true
	}
	return false
}

func (e *mError) ErrorMsg() string {
	msg, ok := errorMsg[e.e]
	if !ok {
		msg = e.msg
	} else {
		msg += " == " + e.msg
	}
	return msg
}

func MError(e pcsError, msg string) *mError {
	return &mError{
		e:   e,
		msg: msg,
	}
}

func MErrorExt(errorCode int, msg string) *mError {
	return &mError{
		e:   pcsError(errorCode),
		msg: msg,
	}
}

// 错误码需要与pcsapi的错误码保持一致
// 变更需谨慎
const (
	NO_ERROR               = pcsError(0)
	API_UNSUPPORTED        = pcsError(3)
	NO_PERMISSION          = pcsError(4)
	UNAUTHORIZED_CLIENT_IP = pcsError(5)
	CDN_REDIRECT           = pcsError(302)

	// db error
	ERROR_DB_QUERY_ERROR      = pcsError(31001)
	ERROR_DB_CONNECT_ERROR    = pcsError(31002)
	ERROR_DB_RESULT_SET_EMPTY = pcsError(31003)
	ERROR_DB_ADD_USER_ROUTER  = pcsError(31004)

	// system error
	ERROR_NETWORK           = pcsError(31021)
	ERROR_SERVER_NOT_ACCESS = pcsError(31022)
	ERROR_PARAM_ERROR       = pcsError(31023)
	ERROR_PCS_INTERNAL      = pcsError(31035)

	// account error
	ERROR_ACCOUNT_BDUSS_INVALID = pcsError(31041)
	ERROR_ACCOUNT_NOT_AUTHORIZE = pcsError(31044)
	ERROR_ACCOUNT_NO_USER       = pcsError(31045)
	ERROR_ACCOUNT_PASS_RELOGIN  = pcsError(31047)

	// file error, from 61 to 80
	ERROR_FILE_NAME_INVALID  = pcsError(31061)
	ERROR_FILE_NOT_AUTHORIZE = pcsError(31064)
	ERROR_FILE_NOT_EXIST     = pcsError(31066)

	// thumbnail
	ERROR_THUMBNAIL_PROCESSING = pcsError(31142)

	// stream
	ERROR_STREAM_NOT_AUTHORIZE   = pcsError(31300)
	ERROR_STREAM_INVALID_FILE    = pcsError(31301)
	ERROR_STREAM_INVALID_TYPE    = pcsError(31302)
	ERROR_STREAM_THIRD_FORBIDDEN = pcsError(31303)
	ERROR_STREAM_FILE_TYPE       = pcsError(31304)

	// digest
	ERROR_DIGEST_NOT_MATCH = pcsError(31327)
)

var errorMsg = map[pcsError]string{
	NO_ERROR:               "success",
	API_UNSUPPORTED:        "api unsupported",
	NO_PERMISSION:          "No permission to do this operation",
	UNAUTHORIZED_CLIENT_IP: "Unauthorized client IP address",
	CDN_REDIRECT:           "redirect to cdn",

	ERROR_DB_QUERY_ERROR:      "db query error",
	ERROR_DB_CONNECT_ERROR:    "db connect error",
	ERROR_DB_RESULT_SET_EMPTY: "db result set is empty",
	ERROR_DB_ADD_USER_ROUTER:  "add new user router to db failed",

	ERROR_NETWORK:           "network error",
	ERROR_SERVER_NOT_ACCESS: "can not access server",
	ERROR_PARAM_ERROR:       "param error",
	ERROR_PCS_INTERNAL:      "pcs internal error",

	ERROR_ACCOUNT_BDUSS_INVALID: "bduss is invalid",
	ERROR_ACCOUNT_NOT_AUTHORIZE: "user is not authorized",
	ERROR_ACCOUNT_NO_USER:       "user not exists",
	ERROR_ACCOUNT_PASS_RELOGIN:  "user must relogin",

	ERROR_FILE_NAME_INVALID:  "file name is invalid",
	ERROR_FILE_NOT_AUTHORIZE: "file is not authorized",
	ERROR_FILE_NOT_EXIST:     "file does not exist",

	ERROR_THUMBNAIL_PROCESSING: "thumbnail processing,please wait",

	ERROR_STREAM_NOT_AUTHORIZE:   "stream type is not authorized",
	ERROR_STREAM_INVALID_FILE:    "not stream file",
	ERROR_STREAM_INVALID_TYPE:    "invalid stream type",
	ERROR_STREAM_THIRD_FORBIDDEN: "not allow to access copyright file",
	ERROR_STREAM_FILE_TYPE:       "file type is not supported",

	ERROR_DIGEST_NOT_MATCH: "digest not match",
}

var errorHttpStatus = map[pcsError]int{
	NO_ERROR:               200,
	API_UNSUPPORTED:        400,
	NO_PERMISSION:          403,
	UNAUTHORIZED_CLIENT_IP: 403,
	CDN_REDIRECT:           302,

	ERROR_DB_QUERY_ERROR:      503,
	ERROR_DB_CONNECT_ERROR:    503,
	ERROR_DB_RESULT_SET_EMPTY: 503,
	ERROR_DB_ADD_USER_ROUTER:  503,

	ERROR_NETWORK:           503,
	ERROR_SERVER_NOT_ACCESS: 503,
	ERROR_PARAM_ERROR:       400,
	ERROR_PCS_INTERNAL:      503,

	ERROR_FILE_NAME_INVALID:  400,
	ERROR_FILE_NOT_AUTHORIZE: 403,
	ERROR_FILE_NOT_EXIST:     404,

	ERROR_ACCOUNT_BDUSS_INVALID: 403,
	ERROR_ACCOUNT_NOT_AUTHORIZE: 403,
	ERROR_ACCOUNT_NO_USER:       403,
	ERROR_ACCOUNT_PASS_RELOGIN:  403,

	ERROR_THUMBNAIL_PROCESSING: 404,

	ERROR_STREAM_NOT_AUTHORIZE:   403,
	ERROR_STREAM_INVALID_FILE:    400,
	ERROR_STREAM_INVALID_TYPE:    400,
	ERROR_STREAM_THIRD_FORBIDDEN: 400,
	ERROR_STREAM_FILE_TYPE:       400,

	ERROR_DIGEST_NOT_MATCH: 403,
}
