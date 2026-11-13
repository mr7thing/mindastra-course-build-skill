#!/usr/bin/env bash
# =============================================================================
#  audit_package.py 回归测试
# -----------------------------------------------------------------------------
#  做法：每个 fixture 都是一个最小课程包，只注入**一处**缺陷。
#        基线包 base_clean 必须 0 error / 0 warning；
#        其余每个 fixture 必须恰好命中它针对的那条判据（多一条、少一条都算失败）。
#
#  用法：
#      ./scripts/run_tests.sh          # 全跑，彩色 PASS/FAIL
#      ./scripts/run_tests.sh -v       # 同时打印每个 fixture 的审计输出
#
#  退出码：0 全过；1 有用例失败。
#  重新生成 fixture：python3 scripts/make_fixtures.py
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")"

AUDIT="python3 audit_package.py"
FIXTURES="fixtures"
VERBOSE=0
[ "${1:-}" = "-v" ] && VERBOSE=1

pass=0
fail=0
failures=()

# check <fixture> <期望 error 数> <期望 warning 数> <应出现的子串>
check() {
  local name=$1 want_err=$2 want_warn=$3 needle=$4
  local out
  out=$($AUDIT "$FIXTURES/$name" 2>&1)
  local got_err got_warn
  local summary
  summary=$(printf '%s\n' "$out" | grep -E '^  -> [0-9]+ error\(s\), [0-9]+ warning\(s\)' | tail -1)
  got_err=$(printf '%s' "$summary" | sed -n 's/^  -> \([0-9]\+\) error(s).*/\1/p')
  got_warn=$(printf '%s' "$summary" | sed -n 's/.*, \([0-9]\+\) warning(s).*/\1/p')
  got_err=${got_err:-0}
  got_warn=${got_warn:-0}

  local ok=1 reason=""
  if [ "$got_err" != "$want_err" ] || [ "$got_warn" != "$want_warn" ]; then
    ok=0
    reason="期望 ${want_err}E/${want_warn}W，实际 ${got_err}E/${got_warn}W"
  elif [ -n "$needle" ] && ! printf '%s' "$out" | grep -qF "$needle"; then
    ok=0
    reason="输出缺少预期片段：$needle"
  fi

  if [ "$ok" = 1 ]; then
    echo "  PASS  $name  (${got_err}E/${got_warn}W)"
    pass=$((pass + 1))
  else
    echo "  FAIL  $name  —— $reason"
    fail=$((fail + 1))
    failures+=("$name: $reason")
  fi
  [ "$VERBOSE" = 1 ] && printf '%s\n\n' "$out"
  return 0
}

# check_zip <zip 文件名> —— 与 check 同语义，但直接审 .zip
check_zip() {
  local name=$1 want_err=$2 want_warn=$3 needle=$4
  local out
  out=$($AUDIT "$FIXTURES/$name" 2>&1)
  local summary got_err got_warn
  summary=$(printf '%s\n' "$out" | grep -E '^  -> [0-9]+ error\(s\), [0-9]+ warning\(s\)' | tail -1)
  got_err=$(printf '%s' "$summary" | sed -n 's/^  -> \([0-9]\+\) error(s).*/\1/p')
  got_warn=$(printf '%s' "$summary" | sed -n 's/.*, \([0-9]\+\) warning(s).*/\1/p')
  got_err=${got_err:-0}; got_warn=${got_warn:-0}
  if [ "$got_err" = "$want_err" ] && [ "$got_warn" = "$want_warn" ] \
     && printf '%s' "$out" | grep -qF "$needle"; then
    echo "  PASS  $name  (${got_err}E/${got_warn}W)"
    pass=$((pass + 1))
  else
    echo "  FAIL  $name  —— 期望 ${want_err}E/${want_warn}W 且含「$needle」，实际 ${got_err}E/${got_warn}W"
    fail=$((fail + 1))
    failures+=("$name: zip 判据未命中")
  fi
  [ "$VERBOSE" = 1 ] && printf '%s\n\n' "$out"
  return 0
}

echo "== audit_package.py 回归 =="
[ -d "$FIXTURES" ] || { echo "FATAL: 找不到 $FIXTURES/，先跑 python3 make_fixtures.py" >&2; exit 1; }

# 基线：必须完全干净，否则下面各 fixture 的"恰好命中一条"就没意义
check base_clean            0 0 "OK"

# 字段覆盖与映射
check dup_mapping           0 1 "多个 step 映射到同一字段"
check uncovered_field       1 0 "没有任何 step 的 maps_to 覆盖"
check unprefillable_field   0 1 "平台不支持预填"
check prefill_never_no_reason 1 0 "缺少 prefill_reason"

# 决策证据
check thinking_not_taught   0 1 "没有教它"

# 打包布局（zip：直接审，不解包）
check_zip zip_wrapped.zip   1 0 "多包了一层顶层目录"

echo
if [ "$fail" -eq 0 ]; then
  echo "全部通过：${pass} 个用例"
  exit 0
fi
echo "失败 ${fail} 个，通过 ${pass} 个"
for f in "${failures[@]}"; do echo "  - $f"; done
exit 1
