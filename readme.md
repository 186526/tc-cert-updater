# tc-cert-updater

只是一个简单的脚本用于更新腾云的 SSL 证书 （EdgeOne 客户应该会觉得很有用）

```bash
$ tc-cert-updater
usage: tc-cert-updater.py [-h] [--resourceTypes [RESOURCETYPES ...]] oldCertificateTag pubkey privkey
```

## Usage

你需要提前配置好 `TENCENTCLOUD_SECRET_ID` `TENCENTCLOUD_SECRET_KEY` 两个变量，注意，配置变量的对应用户需授权 `QcloudSSLFullAccess` 策略。

在需要更新的证书上配置 Tag，其 TagName 为 `ssl-tag`，TagValue 请按照你的心情配置。

尝试更新证书时，会同时更新证书下挂的资源（如 EdgeOne）。

```bash
$ tc-cert-updater $TagValue ~/certificate/test/pubkey ~/certificate/test/privkey --resourceTypes teo

old_cert: **guessPlease**
update_cert: {"DeployRecordId": 0, "DeployStatus": 0, "UpdateSyncProgress": [{"ResourceType": "teo", "UpdateSyncProgressRegions": [{"Region": "", "TotalCount": 1, "OffsetCount": 1, "Status": 1}], "Status": 1}], "RequestId": "**"}
delete_cert: {"DeleteResult": true, "TaskId": null, "RequestId": "**"}
new_cert: **guessPlease**
Certificate updated successfully.
```

该工具会帮助你上传一个新的证书（同样包含 Tag）且刷新资源部署，并将老的证书删除。

## License

The program's code is under MIT LICENSE (SEE LICENSE IN LICENSE).
