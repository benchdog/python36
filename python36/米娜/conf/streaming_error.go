/* streaming */
/*
modification history
--------------------
17/8/30, by zenghaofan, create
DESCRIPTION
    
*/
package common

const (
    ERROR_CODE_NO_ERROR = 0
)

const (
    ERROR_CODE_NO_PERMISSION = 4

    ERROR_CODE_PARAM_ERROR = 31023


    //account error, from 41 to 60
    ERROR_ACCOUNT_NOT_AUTHORIZE = 31044
    ERROR_ACCOUNT_NO_USER       = 31045
    ERROR_ACCOUNT_PASS_RELOGIN  = 31047

    ERROR_PARAM_NOAPPID = 31024

    ERROR_STREAM_FILE_TYPE = 31304

    //file error, from 61 to 80
    ERROR_FILE_NOT_AUTHORIZE   = 31064
    ERROR_FILE_NOT_EXIST       = 31066
    ERROR_FILE_GET_META_FAILED = 31071
    ERROR_DIR_NOT_DOWNLOAD     = 31074

    ERROR_BLOOD_SUCKING     = 31326
    ERROR_EXPIRE_TIMEOUT    = 31360
    ERROR_HOTLINK_FORBIDDEN = 31426           // 防盗链返回错误，使用该错误码

    ERROR_SIGN_ERROR                  = 31362
    ERROR_ILLEGAL_FILE_ERROR          = 31390
    ERROR_ILLEGAL_FILE_ERROR_FOR_PCTB = 31396

    ERROR_STREAMING_AUTH_FAILED      = 31344
    ERROR_STREAMING_PARAM_ERROR      = 31340
    ERROR_STREAMING_NEST_ERROR       = 31348
    ERROR_STREAMING_DOWNLOAD_FAILED  = 31349
    ERROR_STREAMING_TRANSCODING      = 31341
    ERROR_STREAMING_REQ_TIMEOUT      = 31345
    ERROR_STREAMING_TRANSCODE_FAILED = 31346
    ERROR_PCS_INTERNAL_ERROR         = 31035
    ERROR_STREAMING_TIME_TOO_LONG    = 31347
    ERROR_STREAMING_ILLEAGL_VIDEO    = 31339
    ERROR_PCS_REFUSE                 = 31034

    ERROR_PCS_FILE_KEY_FAILD         = 33301 // 查询key失败
    ERROR_PCS_VIDEO_FAILD            = 33302 // 校验video失败
    ERROR_PCS_FILE_KEY_NOT_EXIST     = 33303 // 密钥不存在
    //ERROR_NO_URLS             = 39000
)

var errorMsg = map[int]string{
    ERROR_CODE_NO_ERROR: "success",

    ERROR_CODE_NO_PERMISSION: "No permission to do this operation",

    //
    ERROR_CODE_PARAM_ERROR:      "param error",
    ERROR_ACCOUNT_NOT_AUTHORIZE: "user is not authorized",
    ERROR_ACCOUNT_NO_USER:       "user not exists",
    ERROR_ACCOUNT_PASS_RELOGIN:  "user must relogin",

    ERROR_FILE_NOT_AUTHORIZE:   "file is not authorized",
    ERROR_FILE_NOT_EXIST:       "file does not exist",
    ERROR_FILE_GET_META_FAILED: "get file meta failed",
    ERROR_DIR_NOT_DOWNLOAD:     "directory can't be downloaded",

    ERROR_BLOOD_SUCKING:  "anti hotlinking",
    ERROR_EXPIRE_TIMEOUT: "expire time out error",
    ERROR_HOTLINK_FORBIDDEN: "hotlinking forbidden",

    ERROR_SIGN_ERROR:                  "sign error",
    ERROR_ILLEGAL_FILE_ERROR:          "Illegal File",
    ERROR_ILLEGAL_FILE_ERROR_FOR_PCTB: "Illegal File  for Pc Tongbu",

    ERROR_STREAM_FILE_TYPE: "file type is not supported",

    ERROR_STREAMING_AUTH_FAILED      : "transcoding system erro",
    ERROR_STREAMING_PARAM_ERROR      : "param error with transcode request",
    ERROR_STREAMING_NEST_ERROR       : "transcoding system error",
    ERROR_STREAMING_DOWNLOAD_FAILED  : "download file failed",
    ERROR_STREAMING_TRANSCODING      : "be transcoding, please wait and retry",
    ERROR_STREAMING_REQ_TIMEOUT      : "request timeout, please wait and retry",
    ERROR_STREAMING_TRANSCODE_FAILED : "transcode failed with media file",
    ERROR_PCS_INTERNAL_ERROR         : "pcs internal error",
    ERROR_STREAMING_TIME_TOO_LONG    : "video too long",
    ERROR_STREAMING_ILLEAGL_VIDEO    : "illegal video",
    ERROR_PCS_REFUSE                 : "pcs refuse service",

    ERROR_PARAM_NOAPPID              : "app id is empty",

    ERROR_PCS_FILE_KEY_FAILD         : "pcs file cipher query error",
    ERROR_PCS_VIDEO_FAILD            : "pcs video refuse request",
    ERROR_PCS_FILE_KEY_NOT_EXIST     : "pcs file cipher not exist",
    //ERROR_NO_URLS:             "no urls",
}

var errorHttpStatus = map[int]int{

    ERROR_CODE_NO_ERROR : 200,

    ERROR_CODE_NO_PERMISSION: 403,

    ERROR_CODE_PARAM_ERROR: 400,
    ERROR_STREAM_FILE_TYPE: 400,
    ERROR_PARAM_NOAPPID   : 400,

    ERROR_ACCOUNT_NOT_AUTHORIZE: 403,
    ERROR_ACCOUNT_NO_USER:       403,
    ERROR_ACCOUNT_PASS_RELOGIN:  403,

    ERROR_FILE_NOT_AUTHORIZE:   403,
    ERROR_FILE_NOT_EXIST:       404,
    ERROR_FILE_GET_META_FAILED: 503,
    ERROR_DIR_NOT_DOWNLOAD:     403,

    ERROR_BLOOD_SUCKING:  403,
    ERROR_EXPIRE_TIMEOUT: 403,
    ERROR_HOTLINK_FORBIDDEN: 403,

    ERROR_SIGN_ERROR:                  403,
    ERROR_ILLEGAL_FILE_ERROR:          403,
    ERROR_ILLEGAL_FILE_ERROR_FOR_PCTB: 404,

    ERROR_STREAMING_AUTH_FAILED      :403,
    ERROR_STREAMING_PARAM_ERROR      :400,
    ERROR_STREAMING_NEST_ERROR       :503,
    ERROR_STREAMING_DOWNLOAD_FAILED  :503,
    ERROR_STREAMING_TRANSCODING      :400,
    ERROR_STREAMING_REQ_TIMEOUT      :400,
    ERROR_STREAMING_TRANSCODE_FAILED :400,
    ERROR_PCS_INTERNAL_ERROR         :503,
    ERROR_STREAMING_TIME_TOO_LONG    :400,
    ERROR_STREAMING_ILLEAGL_VIDEO    :400,
    ERROR_PCS_REFUSE                 :400,

    ERROR_PCS_FILE_KEY_FAILD         : 500,
    ERROR_PCS_VIDEO_FAILD            : 400,
    ERROR_PCS_FILE_KEY_NOT_EXIST     : 404,
    //ERROR_NO_URLS:             404,
}

var errorInfo = map[int]string{
    ERROR_HOTLINK_FORBIDDEN : "被封禁",
}

var errorRedo = map[int]int{
    ERROR_HOTLINK_FORBIDDEN : 0,
}

func ErrorInfo(code int) string {
    if v, ok := errorInfo[code]; ok {
        return v
    }
    return ""
}

func ErrorRedo(code int) int {
    if v, ok := errorRedo[code]; ok {
        return v
    }
    return 0
}

func ErrorMsg(code int) string {
    return errorMsg[code]
}

func ErrorHttpStatus(code int) int {
    return errorHttpStatus[code]
}
