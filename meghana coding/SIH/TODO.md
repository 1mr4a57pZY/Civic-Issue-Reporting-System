# Map Clarity Improvements

## Current Status: In Progress

### ✅ Completed Tasks:
- [ ] Create TODO tracking file
- [ ] Update submit_report.html with enhanced map settings
- [ ] Update admin.html with improved map controls
- [ ] Test improved street-level clarity
- [ ] Verify zoom controls functionality

### 🔧 Implementation Details:
1. **Enhanced Tile Layer**: Replace basic OpenStreetMap with CartoDB Positron tiles for better street detail
2. **Improved Zoom Controls**: Add zoom control buttons and optimize initial zoom levels
3. **Street-Level Optimization**: Start at zoom level 13 for user form, improve admin zoom calculation
4. **Better Map Controls**: Add scale control, attribution improvements, loading indicators
5. **Enhanced Markers**: Use more visible markers with better precision

### 📝 Files to Modify:
- `templates/submit_report.html` - User report form map improvements
- `templates/admin.html` - Admin dashboard map enhancements

### 🎯 Goals:
- Users can clearly see streets and select precise locations
- Admins get better clarity for viewing report locations
- Maintain all existing functionality (GPS, markers, popups)
- Improve overall user experience with better map controls
