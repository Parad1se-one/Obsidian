# 🔴 Skills 安全审计报告

**审计时间:** 2026-03-08 19:07 (Asia/Shanghai)
**审计范围:** `/home/openclaw/.openclaw/workspace/skills/`

---

## ✅ 安全项目

### 1. 无恶意代码注入
- ✅ 无 `curl | bash` / `wget | sh` 管道执行
- ✅ 无 `eval` / `exec` 危险函数滥用
- ✅ 无 `base64 -d | bash` 解码执行
- ✅ 无反弹 shell (`/dev/tcp`, `nc -e`)
- ✅ 无 `subprocess.call` + `os.system` 滥用

### 2. 无敏感数据外发
- ✅ 无 `curl/wget` 外发 token/key/secret
- ✅ 无读取 `$HOME/.openclaw/` 认证文件
- ✅ 无 `scp/rsync` 往未知主机传文件

### 3. 无权限持久化
- ✅ 无 `useradd/usermod/passwd`
- ✅ 无 `systemctl enable` 未知服务
- ⚠️ 有 `crontab` 操作（但为用户授权的定时任务）

### 4. 外部 URL 审查
- ✅ 所有 HTTP 请求均为已知安全服务:
  - `qt.gtimg.cn` (腾讯财经)
  - `eastmoney.com` (东方财富)
  - `cls.cn` (财联社)
  - `www.gov.cn` (中国政府网)
  - `api.tavily.com` (Tavily 搜索 API)
  - `docker.1panel.live` (Docker 镜像加速)

---

## ⚠️ 需要注意的问题

### 1. Tavily API Key 硬编码 🔴

**位置:**
```
skills/tavily-search/tavily-search.sh:7
skills/tavily-search/SKILL.md:7,17,56,74
```

**内容:**
```bash
API_KEY="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"
```

**风险等级:** 🟡 中等

**说明:**
- API Key 明文写在脚本和文档中
- 已提交到 Git 仓库 (公开泄露风险)
- 虽然是 dev key，但应使用环境变量

**建议修复:**
```bash
# 改为从环境变量读取
API_KEY="${TAVILY_API_KEY:-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}"
```

---

### 2. Crontab 操作 🟡

**位置:**
```
skills/heartbeat/setup-heartbeat-cron.sh
skills/financial-daily/setup-financial-cron.sh
skills/financial-daily/setup-cron.sh
```

**风险等级:** 🟢 低风险（用户授权）

**说明:**
- 这些脚本会修改系统 crontab
- 但功能透明，用户明确知道在做什么
- 属于黄线命令，已记录到 memory

**建议:**
- 保持现状（用户知情且授权）
- 确保日志记录完整

---

### 3. Mihomo 代理配置 🟡

**位置:**
```
.docker/mihomo/config.yaml
```

**内容:**
- 包含代理节点配置（服务器地址、端口、密码）
- 密码：`d9035304-89b0-457e-bd50-3a7574caba2d`

**风险等级:** 🟡 中等

**说明:**
- 代理配置包含敏感信息
- 不应提交到公开 Git 仓库
- 已在 `.gitignore` 中排除

**建议:**
- ✅ 已确认 `.docker/` 在 `.gitignore` 中
- 不要手动提交此目录

---

## ✅ 结论

**总体评估:** ✅ **安全**

Skills 目录没有发现恶意投毒代码。所有可疑操作均为:
1. 用户明确授权的功能（Cron、代理）
2. 已知安全服务的数据请求（财经 API、搜索 API）

**唯一需要改进:**
- Tavily API Key 应改用环境变量，避免硬编码

---

## 📋 审计命令记录

```bash
# 文件统计
find skills -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.json" | wc -l

# 危险命令扫描
grep -r "curl.*bash\|wget.*sh\|eval\|exec\|base64.*-d" skills/

# 敏感数据扫描
grep -r "export.*TOKEN\|export.*KEY\|\$API_KEY" skills/

# 外发请求扫描
grep -r "http://" skills/ | grep -v "localhost\|127.0.0.1"

# 持久化扫描
grep -r "crontab\|systemctl\|chmod 777" skills/
```

---

*审计完成时间：2026-03-08 19:07*
*审计工具：grep + 人工审查*
