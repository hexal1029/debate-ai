# Web UI Testing Guide
## Character Caching & Streaming Output

This guide will walk you through testing both new features using the web UI.

---

## Prerequisites

Make sure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 18+ installed
- ✅ Anthropic API key configured in `backend/.env`

---

## Step 1: Start the Backend Server

Open a **new terminal window** and run:

```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai/backend

# Activate virtual environment
source venv/bin/activate

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Backend is ready** when you see "Application startup complete"

**Keep this terminal running!**

---

## Step 2: Start the Frontend Server

Open a **second terminal window** and run:

```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai/frontend

# Start Next.js development server
npm run dev
```

**Expected output:**
```
> frontend@0.1.0 dev
> next dev

  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.3s
```

✅ **Frontend is ready** when you see "Ready in X.Xs"

**Keep this terminal running too!**

---

## Step 3: Open the Web UI

Open your browser and navigate to:

**http://localhost:3000**

You should see the AI Historical Debate Generator homepage.

---

## Test 1: Character Caching

### Goal: Verify that character profiles are cached and reused

### 3.1 First Debate (Cache Miss)

1. Click **"创建新辩论"** (Create New Debate) button

2. Fill in the form:
   - **辩论者 1**: `孔子`
   - **辩论者 2**: `老子`
   - **辩论话题**: `道的本质`
   - **辩论轮数**: `2` (keep it short for faster testing)
   - **辩论风格**: `casual-chat` (shorter messages)
   - **语言风格**: `现代口语`
   - ✅ **使用角色缓存**: Keep checked

3. Click **"开始辩论"** button

4. **Watch the terminal (backend)** - You should see:
   ```
   ⟳ 正在研究角色 孔子（缓存未命中，将保存到缓存）...
   ⟳ 正在研究角色 老子（缓存未命中，将保存到缓存）...
   ```

5. **Watch the browser** - You should see:
   - Progress indicator showing steps
   - Messages streaming in real-time with blinking cursor `|`
   - Messages appearing gradually, not all at once

6. **Verify cache files created:**
   ```bash
   # In a third terminal
   ls -la /Users/ddhuang/Desktop/CUR/debate-ai/cache/characters/
   ```

   **Expected:**
   ```
   孔子_zh.json
   老子_zh.json
   ```

### 3.2 Second Debate (Cache Hit)

1. Click **"返回"** (Back) button to go to homepage

2. Click **"创建新辩论"** again

3. Fill in the form with **SAME characters, DIFFERENT topic**:
   - **辩论者 1**: `孔子`
   - **辩论者 2**: `老子`
   - **辩论话题**: `治国之道` ← **DIFFERENT topic**
   - **辩论轮数**: `2`
   - **辩论风格**: `casual-chat`
   - ✅ **使用角色缓存**: Keep checked

4. Click **"开始辩论"**

5. **Watch the terminal (backend)** - You should see:
   ```
   ✓ 使用缓存的角色资料: 孔子
   ✓ 使用缓存的角色资料: 老子
   ```

6. **Notice the speed difference:**
   - First debate: ~15 seconds to start (character research)
   - Second debate: ~1 second to start (cache hit!)
   - **This is 10-15x faster for character loading!** ⚡

### 3.3 Test Cache Disable

1. Go back and create a **third debate**

2. Fill in the same characters:
   - **辩论者 1**: `孔子`
   - **辩论者 2**: `老子`
   - **辩论话题**: `仁义礼智`
   - ❌ **使用角色缓存**: **UNCHECK this box**

3. Click **"开始辩论"**

4. **Watch the terminal** - Even though cache exists, you should see:
   ```
   ⟳ 正在研究角色 孔子（缓存已禁用）...
   ⟳ 正在研究角色 老子（缓存已禁用）...
   ```

5. **This proves the cache toggle works!** ✅

---

## Test 2: Streaming Output

### Goal: Verify real-time token-by-token streaming

### 4.1 Watch the Streaming in Action

1. Create a new debate (reuse孔子 and 老子 with cache enabled for speed)

2. **Open Browser DevTools**:
   - Press `F12` or `Cmd+Option+I` (Mac)
   - Go to **Network** tab
   - Filter by "EventStream" or look for `stream` in the name

3. Click **"开始辩论"**

4. **In the Network tab**, click on the streaming connection (should be something like `/api/debates/deb_xxx/stream`)

5. **Watch the EventStream tab** - You should see events arriving in real-time:
   ```
   event: progress
   data: {"step":"2/7","message":"正在研究 孔子 的背景和思想..."}

   event: partial_message
   data: {"speaker":"主持人","role":"moderator","content":"欢","is_complete":false}

   event: partial_message
   data: {"speaker":"主持人","role":"moderator","content":"欢迎","is_complete":false}

   event: partial_message
   data: {"speaker":"主持人","role":"moderator","content":"欢迎来到","is_complete":false}

   event: message
   data: {"speaker":"主持人","role":"moderator","content":"欢迎来到...","is_complete":true}
   ```

6. **In the browser UI**, watch for:
   - ✅ Blinking cursor `|` at the end of the currently streaming message
   - ✅ Text appearing gradually, character by character
   - ✅ Smooth animation (not choppy)
   - ✅ Cursor disappears when message is complete
   - ✅ Next message starts streaming immediately

### 4.2 Visual Indicators Checklist

While watching the debate stream, verify:

- [ ] **Blinking cursor visible** during message generation
- [ ] **Cursor animates** (pulses/blinks)
- [ ] **Text builds up** gradually (not all at once)
- [ ] **Cursor disappears** when message is complete
- [ ] **Auto-scroll** keeps new content in view
- [ ] **Different colored backgrounds** for moderator vs characters
- [ ] **Smooth transitions** between messages

### 4.3 Test Multiple Messages

1. Watch the entire debate (2 rounds = ~8-10 messages total)

2. **Verify each message streams:**
   - Moderator opening → streams
   - Character 1 opening → streams
   - Character 2 opening → streams
   - Round 1, Character 1 → streams
   - Round 1, Character 2 → streams
   - Round 2, Character 1 → streams
   - Round 2, Character 2 → streams
   - Moderator closing → streams

3. **All messages should stream, not just characters!**

---

## Test 3: Combined Features

### Goal: Verify caching and streaming work together seamlessly

### 5.1 Quick Iteration Test

1. Create debate: `孔子` vs `老子`, topic: `道`, rounds: `2`
   - First time: ~45 seconds total (research 15s + debate 30s)
   - Watch: Character research + streaming messages

2. Create debate: `孔子` vs `老子`, topic: `礼`, rounds: `2`
   - Second time: ~30 seconds total (cache 1s + debate 30s)
   - Watch: Cache hit + streaming messages

3. Create debate: `孔子` vs `老子`, topic: `仁`, rounds: `2`
   - Third time: ~30 seconds total
   - Watch: Cache hit + streaming messages

**Result:** You should see:
- ✅ Faster subsequent debates (caching works)
- ✅ All debates still stream (streaming works)
- ✅ No conflicts or errors (integration works)

### 5.2 Different Characters Test

1. Create debate: `牛顿` vs `爱因斯坦`, topic: `时间`, rounds: `2`
   - Watch: Research new characters + streaming

2. Create debate: `牛顿` vs `爱因斯坦`, topic: `空间`, rounds: `2`
   - Watch: Use cached characters + streaming

3. Create debate: `孔子` vs `牛顿`, topic: `科学与哲学`, rounds: `2`
   - Watch: One cached (孔子), one cached (牛顿) + streaming

**Result:** Mixed cache hits/misses should work seamlessly ✅

---

## Test 4: Edge Cases

### 6.1 Name Variations (Cache Normalization)

Test that name variations hit the same cache:

1. Create debate: `孔子` vs `老子`
   - Should use cache ✅

2. Create debate: `孔 子` vs `老 子` (with spaces)
   - Should use cache ✅ (same normalized key)

3. Create debate: `Newton` vs `Einstein`
   - Should miss cache (new characters)

4. Create debate: `newton` vs `einstein` (lowercase)
   - Should use cache ✅ (case-insensitive normalization)

### 6.2 Network Interruption

Test reconnection:

1. Start a debate

2. **Disconnect your internet** mid-stream

3. **Reconnect internet** after 5-10 seconds

4. **Watch**: EventSource should auto-reconnect and resume

   **Expected behavior:**
   - Connection lost → `status: 'error'`
   - Connection restored → Reconnects automatically
   - Streaming may resume or show error (depends on timing)

### 6.3 Concurrent Debates

Test multiple debates at once:

1. Open **two browser tabs** side-by-side

2. In **Tab 1**: Create debate `孔子` vs `老子`, topic: `道`

3. In **Tab 2**: Create debate `牛顿` vs `爱因斯坦`, topic: `时间`

4. **Watch both tabs stream simultaneously**

   **Expected:**
   - ✅ Both debates stream independently
   - ✅ No cross-contamination (messages don't mix)
   - ✅ No crashes or errors

---

## Troubleshooting

### Backend Issues

**Problem:** Backend won't start

**Solutions:**
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process if needed
kill -9 <PID>

# Try starting again
cd backend && source venv/bin/activate && uvicorn main:app --reload
```

**Problem:** API key errors

**Solution:**
```bash
# Check .env file has valid API key
cat backend/.env | grep ANTHROPIC_API_KEY

# Should show: ANTHROPIC_API_KEY="sk-ant-..."
```

### Frontend Issues

**Problem:** Frontend won't start

**Solutions:**
```bash
# Check if port 3000 is in use
lsof -i :3000

# Reinstall dependencies if needed
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Problem:** "Cannot connect to backend"

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/api/styles

# Should return JSON with debate styles
```

### Streaming Issues

**Problem:** Messages not streaming, appearing all at once

**Check:**
1. Backend terminal - should see no errors
2. Browser DevTools → Console - check for errors
3. Browser DevTools → Network → EventStream tab - should see `partial_message` events

**Solution:**
```bash
# Restart both servers
# Backend: Ctrl+C, then uvicorn main:app --reload
# Frontend: Ctrl+C, then npm run dev
# Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

**Problem:** Blinking cursor not visible

**Check:**
1. Inspect element - should have `animate-pulse` class
2. Check if Tailwind CSS loaded

**Solution:**
```bash
# Rebuild frontend
cd frontend
npm run build
npm run dev
```

### Cache Issues

**Problem:** Cache not being used (always showing "研究角色")

**Check:**
```bash
# Verify cache files exist
ls -la cache/characters/

# Check file contents
cat cache/characters/孔子_zh.json
```

**Solution:**
```bash
# Clear cache and try again
rm -rf cache/characters/*

# Or use CLI to clear specific character
python3 debate.py --clear-cache "孔子"
```

---

## Success Checklist

After completing all tests, you should have verified:

### Character Caching ✅
- [ ] First debate creates cache files
- [ ] Second debate uses cache (much faster)
- [ ] Cache files exist in `cache/characters/`
- [ ] Terminal shows "✓ 使用缓存的角色资料"
- [ ] Name variations hit same cache
- [ ] Cache toggle (checkbox) works
- [ ] Disabling cache forces fresh research

### Streaming Output ✅
- [ ] Messages appear gradually, not all at once
- [ ] Blinking cursor visible during streaming
- [ ] Cursor animates (pulses)
- [ ] Cursor disappears when message complete
- [ ] All messages stream (moderator + characters)
- [ ] DevTools shows `partial_message` events
- [ ] Auto-scroll keeps content in view
- [ ] Smooth animations, no flickering

### Integration ✅
- [ ] Cached debates still stream properly
- [ ] Non-cached debates stream properly
- [ ] No errors in browser console
- [ ] No errors in backend terminal
- [ ] Concurrent debates work independently
- [ ] Page refreshes work correctly

---

## Performance Measurements

Record your observations:

**First debate (cache miss):**
- Time to start generating: _____ seconds (expected: ~15s)
- Total time: _____ seconds (expected: ~45s)
- Perceived wait (when you see first content): _____ seconds (expected: ~15s)

**Second debate (cache hit):**
- Time to start generating: _____ seconds (expected: ~1s)
- Total time: _____ seconds (expected: ~30s)
- Perceived wait: _____ seconds (expected: ~1s)

**Streaming experience:**
- Blinking cursor visible: Yes / No
- Text appears gradually: Yes / No
- Feels responsive: Yes / No

---

## Video Recording (Optional)

For documentation, consider recording your screen:

**Mac:**
- Press `Cmd+Shift+5` → Select screen recording
- Record a full debate from start to finish

**Windows:**
- Press `Win+G` → Click record button

**What to capture:**
- Creating a debate
- Streaming messages with blinking cursor
- Cache hit message in terminal
- DevTools EventStream tab

---

## Next Steps

After testing:

1. ✅ Review `FEATURES_CACHE_STREAMING.md` for implementation details
2. ✅ Check `IMPLEMENTATION_SUMMARY.md` for architecture overview
3. 📝 Report any issues or unexpected behavior
4. 🚀 Use the web UI to generate awesome debates!

---

## Quick Reference

**Start Backend:**
```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai/backend
source venv/bin/activate
uvicorn main:app --reload
```

**Start Frontend:**
```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai/frontend
npm run dev
```

**Open Browser:**
```
http://localhost:3000
```

**Check Cache:**
```bash
ls -la /Users/ddhuang/Desktop/CUR/debate-ai/cache/characters/
```

**Clear Cache:**
```bash
rm -rf /Users/ddhuang/Desktop/CUR/debate-ai/cache/characters/*
```

---

**Happy Testing! 🎉**

If you encounter any issues, check the Troubleshooting section above or review the comprehensive documentation in `FEATURES_CACHE_STREAMING.md`.
