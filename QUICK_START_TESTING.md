# Quick Start - Web UI Testing

## 🚀 Start in 3 Steps

### Step 1: Start Backend (Terminal 1)

```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai
./start_backend.sh
```

**Wait for:** `Application startup complete.`

✅ Backend running on **http://localhost:8000**

---

### Step 2: Start Frontend (Terminal 2)

Open a **NEW terminal** and run:

```bash
cd /Users/ddhuang/Desktop/CUR/debate-ai
./start_frontend.sh
```

**Wait for:** `✓ Ready in X.Xs`

✅ Frontend running on **http://localhost:3000**

---

### Step 3: Open Browser

Navigate to: **http://localhost:3000**

---

## 🧪 Quick Tests

### Test 1: Character Caching (2 minutes)

**First Debate (creates cache):**
1. Click "创建新辩论"
2. Fill in:
   - 辩论者1: `孔子`
   - 辩论者2: `老子`
   - 话题: `道的本质`
   - 轮数: `2`
   - ✅ 使用角色缓存 (keep checked)
3. Click "开始辩论"
4. **Watch backend terminal:** Should see `⟳ 正在研究角色...（缓存未命中）`
5. Wait ~45 seconds for completion

**Second Debate (uses cache):**
1. Go back, create new debate
2. Fill in:
   - 辩论者1: `孔子` (same)
   - 辩论者2: `老子` (same)
   - 话题: `治国之道` (different)
   - 轮数: `2`
3. Click "开始辩论"
4. **Watch backend terminal:** Should see `✓ 使用缓存的角色资料`
5. **Notice:** Starts MUCH faster (~1 second vs 15 seconds)

✅ **Success:** Second debate starts 10-15x faster!

---

### Test 2: Streaming Output (1 minute)

**Watch for streaming indicators:**

1. Create any debate
2. While debate is generating, look for:
   - ✅ Text appearing gradually (not all at once)
   - ✅ Blinking cursor `|` at end of current message
   - ✅ Cursor disappears when message completes
   - ✅ Next message starts streaming immediately

**Open DevTools (optional):**
1. Press `F12` or `Cmd+Option+I`
2. Go to **Network** tab → Filter "EventStream"
3. Click the `/stream` connection
4. **Watch:** `partial_message` events arriving in real-time

✅ **Success:** You see text building up character-by-character!

---

## 📊 What to Observe

### Backend Terminal

**First debate (cache miss):**
```
[2/7] 正在研究 孔子 的背景和思想...
⟳ 正在研究角色 孔子（缓存未命中，将保存到缓存）...
[3/7] 正在研究 老子 的背景和思想...
⟳ 正在研究角色 老子（缓存未命中，将保存到缓存）...
```

**Second debate (cache hit):**
```
[2/7] 正在研究 孔子 的背景和思想...
✓ 使用缓存的角色资料: 孔子
[3/7] 正在研究 老子 的背景和思想...
✓ 使用缓存的角色资料: 老子
```

### Browser UI

**Streaming in action:**
1. Message appears empty
2. Text starts appearing: "欢"
3. More text: "欢迎"
4. Blinking cursor at end: "欢迎来到今天的辩论|"
5. Text continues building up
6. Cursor disappears when complete
7. Next message starts immediately

### Cache Files

Check cache was created:
```bash
ls -la cache/characters/
```

**Expected output:**
```
孔子_zh.json
老子_zh.json
```

---

## 🎯 Success Criteria

You've successfully tested both features when you see:

✅ **Caching:**
- [ ] Terminal shows cache miss first time
- [ ] Terminal shows cache hit second time
- [ ] Second debate starts much faster
- [ ] Cache files exist in `cache/characters/`

✅ **Streaming:**
- [ ] Text appears gradually, not all at once
- [ ] Blinking cursor visible during generation
- [ ] Cursor disappears when message complete
- [ ] All messages stream (moderator + characters)

---

## 🐛 Troubleshooting

**Backend won't start:**
```bash
# Kill any existing process on port 8000
lsof -i :8000
kill -9 <PID>

# Try again
./start_backend.sh
```

**Frontend won't start:**
```bash
# Kill any existing process on port 3000
lsof -i :3000
kill -9 <PID>

# Try again
./start_frontend.sh
```

**Streaming not working:**
1. Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Check browser console (F12) for errors
3. Check backend terminal for errors

**Cache not working:**
```bash
# Clear cache and try again
rm -rf cache/characters/*
```

---

## 📚 Full Documentation

For detailed testing instructions, see:
- **WEB_UI_TESTING_GUIDE.md** - Comprehensive testing guide
- **FEATURES_CACHE_STREAMING.md** - Complete feature documentation
- **IMPLEMENTATION_SUMMARY.md** - Implementation overview

---

## 🎬 Ready to Test!

**Run these two commands in separate terminals:**

Terminal 1:
```bash
./start_backend.sh
```

Terminal 2:
```bash
./start_frontend.sh
```

**Then open:** http://localhost:3000

**Have fun testing!** 🎉
