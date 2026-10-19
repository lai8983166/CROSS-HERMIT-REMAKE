// Owned x86 screen DC, timer samples and first startup font. No window or drawing.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Web.Script.Serialization;

class SchoolFontStateGDIv4 {
 [DllImport("user32.dll")] static extern IntPtr GetDC(IntPtr window);
 [DllImport("user32.dll")] static extern int ReleaseDC(IntPtr window,IntPtr dc);
 [DllImport("kernel32.dll")] static extern bool QueryPerformanceCounter(out long value);
 [DllImport("kernel32.dll")] static extern bool QueryPerformanceFrequency(out long value);
 [DllImport("kernel32.dll")] static extern uint GetACP();
 [DllImport("gdi32.dll")] static extern IntPtr CreateFontA(int height,int width,int angle,int orientation,int weight,uint italic,uint underline,uint strike,uint charset,uint precision,uint clip,uint quality,uint family,IntPtr face);
 [DllImport("gdi32.dll")] static extern int GetObjectA(IntPtr obj,int count,IntPtr output);
 [DllImport("gdi32.dll")] static extern bool DeleteObject(IntPtr obj);
 [DllImport("gdi32.dll")] static extern IntPtr CreateCompatibleDC(IntPtr dc);
 [DllImport("gdi32.dll")] static extern IntPtr CreateDIBSection(IntPtr dc,IntPtr info,uint usage,out IntPtr bits,IntPtr section,uint offset);
 [DllImport("gdi32.dll")] static extern IntPtr SelectObject(IntPtr dc,IntPtr obj);
 [DllImport("gdi32.dll")] static extern int SetBkMode(IntPtr dc,int mode);
 [DllImport("gdi32.dll")] static extern uint SetBkColor(IntPtr dc,uint color);
 [DllImport("gdi32.dll")] static extern uint SetTextColor(IntPtr dc,uint color);
 [DllImport("gdi32.dll")] static extern IntPtr CreateFontIndirectA(IntPtr logfont);
 [DllImport("gdi32.dll")] static extern bool DeleteDC(IntPtr dc);
 [DllImport("gdi32.dll")] static extern int SetMapMode(IntPtr dc,int mode);
 [DllImport("gdi32.dll")] static extern uint SetTextAlign(IntPtr dc,uint align);
 [DllImport("kernel32.dll")] static extern int MulDiv(int number,int numerator,int denominator);
 [DllImport("gdi32.dll")] static extern bool GetTextExtentPoint32A(IntPtr dc,IntPtr text,int count,IntPtr output);
 [DllImport("gdi32.dll")] static extern bool ExtTextOutA(IntPtr dc,int x,int y,uint options,IntPtr rect,IntPtr text,uint count,IntPtr spacing);
 [DllImport("gdi32.dll")] static extern bool GdiFlush();
 [DllImport("gdi32.dll")] static extern uint GetObjectType(IntPtr obj);
 [DllImport("gdi32.dll")] static extern IntPtr GetCurrentObject(IntPtr dc,uint type);
 static int nativeCleanupStep,nativeBitmapReleased,nativeDCReleased,nativeFontReleased;static bool bitmapDeleteIssued,fontDeleteIssued;
 static int glyphIndex,snapshotMask,penX,penY,glyphWidth,glyphHeight;static bool awaitingDraw;
 static IntPtr atlasDC,atlasBitmap,atlasBits,atlasFont,atlasOldBitmap,atlasOldFont;static int atlasStep;
 static IntPtr cacheDC,cacheBitmap,cacheBits,oldBitmap,indirectFont;static int cacheStep;static string sourceLogfont;
 static IntPtr dc,font;static long sequence;
 static JavaScriptSerializer json=new JavaScriptSerializer();
 static uint Pointer(IntPtr p){return unchecked((uint)p.ToInt32());}
 static string Hex(byte[] b){return BitConverter.ToString(b).Replace("-","").ToLowerInvariant();}
 static uint Number(Dictionary<string,object> r,string key) {
  object o=r[key];if(!(o is int) && !(o is long))throw new ArgumentException("integer required");
  long value=Convert.ToInt64(o);if(value<0 || value>uint.MaxValue)throw new ArgumentException("uint32 required");return (uint)value;
 }
 static void Keys(Dictionary<string,object> r,params string[] keys) {
  if(r.Count!=keys.Length)throw new ArgumentException("request shape");foreach(string key in keys)if(!r.ContainsKey(key))throw new ArgumentException("request shape");
 }
 static int LiveBytes(IntPtr obj){IntPtr p=Marshal.AllocHGlobal(60);try{Marshal.Copy(new byte[60],0,p,60);return GetObjectA(obj,60,p);}finally{Marshal.FreeHGlobal(p);}}
 static object Cleanup() {
  int fonts=0,dcs=0,bitmaps=0,cacheDcs=0;bool ok=true,restored=true;
  int atlasFonts=0,atlasDcs=0,atlasBitmaps=0;bool atlasRestored=true;
  if(atlasBitmap!=IntPtr.Zero && bitmapDeleteIssued && LiveBytes(atlasBitmap)==0){
   nativeBitmapReleased++;atlasBitmap=IntPtr.Zero;atlasBits=IntPtr.Zero;
   if(atlasDC!=IntPtr.Zero && atlasOldBitmap!=IntPtr.Zero){
    if(GetCurrentObject(atlasDC,7)!=atlasOldBitmap)SelectObject(atlasDC,atlasOldBitmap);
    atlasRestored&=GetCurrentObject(atlasDC,7)==atlasOldBitmap;atlasOldBitmap=IntPtr.Zero;
   }
  }
  if(atlasDC!=IntPtr.Zero && atlasOldFont!=IntPtr.Zero){atlasRestored&=SelectObject(atlasDC,atlasOldFont)==atlasFont;atlasOldFont=IntPtr.Zero;}
  if(atlasDC!=IntPtr.Zero && atlasOldBitmap!=IntPtr.Zero){atlasRestored&=SelectObject(atlasDC,atlasOldBitmap)==atlasBitmap;atlasOldBitmap=IntPtr.Zero;}
  ok&=atlasRestored;
  if(atlasFont!=IntPtr.Zero && fontDeleteIssued && LiveBytes(atlasFont)==0){nativeFontReleased++;atlasFont=IntPtr.Zero;}
  if(atlasBitmap!=IntPtr.Zero && bitmapDeleteIssued && LiveBytes(atlasBitmap)==0){nativeBitmapReleased++;atlasBitmap=IntPtr.Zero;atlasBits=IntPtr.Zero;}
  if(atlasFont!=IntPtr.Zero){bool r=DeleteObject(atlasFont);ok&=r;if(r)atlasFonts++;atlasFont=IntPtr.Zero;}
  if(atlasBitmap!=IntPtr.Zero){bool r=DeleteObject(atlasBitmap);ok&=r;if(r)atlasBitmaps++;atlasBitmap=IntPtr.Zero;atlasBits=IntPtr.Zero;}
  if(atlasDC!=IntPtr.Zero){bool r=DeleteDC(atlasDC);ok&=r;if(r)atlasDcs++;atlasDC=IntPtr.Zero;}
  if(cacheDC!=IntPtr.Zero && oldBitmap!=IntPtr.Zero){restored=SelectObject(cacheDC,oldBitmap)==cacheBitmap;ok&=restored;oldBitmap=IntPtr.Zero;}
  if(cacheBitmap!=IntPtr.Zero){bool r=DeleteObject(cacheBitmap);ok&=r;if(r)bitmaps++;cacheBitmap=IntPtr.Zero;cacheBits=IntPtr.Zero;}
  if(cacheDC!=IntPtr.Zero){bool r=DeleteDC(cacheDC);ok&=r;if(r)cacheDcs++;cacheDC=IntPtr.Zero;}
  if(indirectFont!=IntPtr.Zero){bool r=DeleteObject(indirectFont);ok&=r;if(r)fonts++;indirectFont=IntPtr.Zero;}
  if(font!=IntPtr.Zero){bool result=DeleteObject(font);ok&=result;if(result)fonts++;font=IntPtr.Zero;}
  if(dc!=IntPtr.Zero){int result=ReleaseDC(IntPtr.Zero,dc);ok&=result==1;if(result==1)dcs++;dc=IntPtr.Zero;}
  return new {native_atlas_fonts_released=nativeFontReleased,native_atlas_dcs_released=nativeDCReleased,native_atlas_bitmaps_released=nativeBitmapReleased,native_bitmap_delete_issued=bitmapDeleteIssued,native_cleanup_completed=nativeCleanupStep==3,atlas_fonts_released=atlasFonts,atlas_dcs_released=atlasDcs,atlas_bitmaps_released=atlasBitmaps,atlas_selection_restored=atlasRestored,fonts_released=fonts,dcs_released=dcs,cache_bitmaps_released=bitmaps,cache_dcs_released=cacheDcs,cache_selection_restored=restored,all_owned_resources_released=ok};
 }
 static object Dispatch(Dictionary<string,object> r) {
  string op=(string)r["op"];
  if(op=="GetDC") {
   Keys(r,"id","op");if(dc!=IntPtr.Zero)throw new ArgumentException("one owned screen DC");dc=GetDC(IntPtr.Zero);
   if(dc==IntPtr.Zero)throw new InvalidOperationException("real GetDC failed");return new {result=Pointer(dc)};
  }
  if(op=="QueryPerformanceCounter" || op=="QueryPerformanceFrequency") {
   Keys(r,"id","op");long value;bool ok=op=="QueryPerformanceCounter"?QueryPerformanceCounter(out value):QueryPerformanceFrequency(out value);
   if(!ok || value<=0)throw new InvalidOperationException("real timer failed");return new {result=1,hex=Hex(BitConverter.GetBytes(value))};
  }
  if(op=="CreateFontA") {
   Keys(r,"id","op","args","face_hex");if(font!=IntPtr.Zero)throw new ArgumentException("one owned startup font");
   IList a=r["args"] as IList;long[] expected={0,0,0,0,700,0,0,0,1,5,0,0,0};
   if(a==null || a.Count!=13 || (string)r["face_hex"]!="b2d3a9fac5e920")throw new ArgumentException("original startup font request");
   for(int i=0;i<13;i++)if(Convert.ToInt64(a[i])!=expected[i])throw new ArgumentException("original startup font arguments");
   byte[] face={0xb2,0xd3,0xa9,0xfa,0xc5,0xe9,0x20,0};IntPtr p=Marshal.AllocHGlobal(face.Length);
   try{Marshal.Copy(face,0,p,face.Length);font=CreateFontA(0,0,0,0,700,0,0,0,1,5,0,0,0,p);}finally{Marshal.FreeHGlobal(p);}
   if(font==IntPtr.Zero)throw new InvalidOperationException("real startup font failed");return new {result=Pointer(font)};
  }
  if(op=="GetObjectA") {
   Keys(r,"id","op","pointer","before_hex");if(font==IntPtr.Zero || Number(r,"pointer")!=Pointer(font))throw new ArgumentException("owned live font required");
   string initial=(string)r["before_hex"];if(initial.Length!=120)throw new ArgumentException("exact initial LOGFONT buffer");
   byte[] before=new byte[60];for(int i=0;i<60;i++)before[i]=Convert.ToByte(initial.Substring(i*2,2),16);
   IntPtr p=Marshal.AllocHGlobal(60);try {
    Marshal.Copy(before,0,p,60);
    int count=GetObjectA(font,60,p);if(count!=60)throw new InvalidOperationException("complete real LOGFONTA required");
    byte[] b=new byte[60];Marshal.Copy(p,b,0,60);sourceLogfont=Hex(b);return new {result=count,hex=sourceLogfont};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="CreateCompatibleDC") {
   Keys(r,"id","op");if(cacheStep!=0 || dc==IntPtr.Zero)throw new ArgumentException("one owned cache DC");cacheDC=CreateCompatibleDC(IntPtr.Zero);
   if(cacheDC==IntPtr.Zero)throw new InvalidOperationException("actual cache DC failed");cacheStep=1;return new {result=Pointer(cacheDC)};
  }
  if(op=="CreateDIBSection") {
   Keys(r,"id","op","pointer","header_hex");if(cacheStep!=1 || Number(r,"pointer")!=Pointer(cacheDC))throw new ArgumentException("owned cache DC/header order");
   string text=(string)r["header_hex"];if(text.Length!=80)throw new ArgumentException("complete40-byte DIB header");
   byte[] b=new byte[40];for(int i=0;i<40;i++)b[i]=Convert.ToByte(text.Substring(i*2,2),16);
   byte[] expected=new byte[40];Array.Copy(BitConverter.GetBytes(40),0,expected,0,4);Array.Copy(BitConverter.GetBytes(256),0,expected,4,4);Array.Copy(BitConverter.GetBytes(-256),0,expected,8,4);expected[12]=1;expected[14]=32;
   if(Hex(b)!=Hex(expected))throw new ArgumentException("original top-down32-bit cache bitmap");
   IntPtr p=Marshal.AllocHGlobal(40);try{Marshal.Copy(b,0,p,40);cacheBitmap=CreateDIBSection(cacheDC,p,0,out cacheBits,IntPtr.Zero,0);}finally{Marshal.FreeHGlobal(p);}
   if(cacheBitmap==IntPtr.Zero || cacheBits==IntPtr.Zero)throw new InvalidOperationException("actual DIB failed");cacheStep=2;return new {result=Pointer(cacheBitmap),bits=Pointer(cacheBits)};
  }
  if(op=="SetBkMode" || op=="SetBkColor" || op=="SetTextColor") {
   Keys(r,"id","op","pointer","value");uint value=Number(r,"value");
   int expectedStep=op=="SetBkMode"?2:op=="SetBkColor"?3:4;uint expectedValue=op=="SetBkMode"?2u:op=="SetBkColor"?0u:0xffffffu;
   if(cacheStep!=expectedStep || Number(r,"pointer")!=Pointer(cacheDC) || value!=expectedValue)throw new ArgumentException("original cache DC state");
   uint result=op=="SetBkMode"?(uint)SetBkMode(cacheDC,(int)value):op=="SetBkColor"?SetBkColor(cacheDC,value):SetTextColor(cacheDC,value);
   if(result==uint.MaxValue || (op=="SetBkMode" && result==0))throw new InvalidOperationException("actual GDI state failed");cacheStep++;return new {result=result};
  }
  if(op=="SelectObject") {
   Keys(r,"id","op","pointer","object");if(cacheStep!=5 || Number(r,"pointer")!=Pointer(cacheDC) || Number(r,"object")!=Pointer(cacheBitmap))throw new ArgumentException("owned cache bitmap selection");
   oldBitmap=SelectObject(cacheDC,cacheBitmap);if(oldBitmap==IntPtr.Zero || oldBitmap.ToInt32()==-1)throw new InvalidOperationException("actual bitmap selection failed");cacheStep=6;return new {result=Pointer(oldBitmap)};
  }
  if(op=="CreateFontIndirectA") {
   Keys(r,"id","op","logfont_hex");string text=(string)r["logfont_hex"];
   if(cacheStep!=6 || sourceLogfont==null || text!=sourceLogfont || indirectFont!=IntPtr.Zero)throw new ArgumentException("complete original owned LOGFONT required");
   byte[] b=new byte[60];for(int i=0;i<60;i++)b[i]=Convert.ToByte(text.Substring(i*2,2),16);
   IntPtr p=Marshal.AllocHGlobal(60);try {
    Marshal.Copy(b,0,p,60);indirectFont=CreateFontIndirectA(p);if(indirectFont==IntPtr.Zero)throw new InvalidOperationException("actual indirect font failed");
    int count=GetObjectA(indirectFont,60,p);byte[] actual=new byte[60];Marshal.Copy(p,actual,0,60);cacheStep=7;
    return new {result=Pointer(indirectFont),inspection=new {native_requested=false,method="GetObjectA",result=count,hex=Hex(actual)}};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="atlas_dc") {
   Keys(r,"id","op");if(cacheStep!=7 || atlasStep!=0)throw new ArgumentException("one separate atlas DC after original cache/font");
   atlasDC=CreateCompatibleDC(IntPtr.Zero);if(atlasDC==IntPtr.Zero)throw new InvalidOperationException("actual atlas DC failed");atlasStep=1;return new {result=Pointer(atlasDC)};
  }
  if(op=="atlas_dib") {
   Keys(r,"id","op","pointer","header_hex");if(atlasStep!=1 || Number(r,"pointer")!=Pointer(atlasDC))throw new ArgumentException("original atlas DIB order/owner");
   string text=(string)r["header_hex"];byte[] expected=new byte[40];Array.Copy(BitConverter.GetBytes(40),0,expected,0,4);Array.Copy(BitConverter.GetBytes(256),0,expected,4,4);Array.Copy(BitConverter.GetBytes(-256),0,expected,8,4);expected[12]=1;expected[14]=32;
   if(text!=Hex(expected))throw new ArgumentException("complete original atlas top-down DIB header");
   IntPtr p=Marshal.AllocHGlobal(40);try{Marshal.Copy(expected,0,p,40);atlasBitmap=CreateDIBSection(atlasDC,p,0,out atlasBits,IntPtr.Zero,0);}finally{Marshal.FreeHGlobal(p);}
   if(atlasBitmap==IntPtr.Zero || atlasBits==IntPtr.Zero)throw new InvalidOperationException("actual atlas DIB failed");atlasStep=2;return new {result=Pointer(atlasBitmap),bits=Pointer(atlasBits)};
  }
  if(op=="atlas_muldiv") {
   Keys(r,"id","op","args");IList a=r["args"] as IList;long[] expected={12,96,72};
   if(atlasStep!=3 || a==null || a.Count!=3)throw new ArgumentException("original atlas MulDiv order");
   for(int i=0;i<3;i++)if(Convert.ToInt64(a[i])!=expected[i])throw new ArgumentException("original atlas MulDiv args");
   int value=MulDiv(12,96,72);if(value!=16)throw new InvalidOperationException("actual atlas MulDiv failed");atlasStep=4;return new {result=value};
  }
  if(op=="atlas_font") {
   Keys(r,"id","op","args","face_hex");IList a=r["args"] as IList;long[] expected={-16,0,0,0,700,0,0,0,1,0,0,4,2};
   if(atlasStep!=4 || a==null || a.Count!=13 || (string)r["face_hex"]!="4669786564537973")throw new ArgumentException("original atlas font order/face");
   for(int i=0;i<13;i++)if(Convert.ToInt64(a[i])!=expected[i])throw new ArgumentException("original atlas font arguments");
   byte[] face=System.Text.Encoding.ASCII.GetBytes("FixedSys\0");IntPtr p=Marshal.AllocHGlobal(60);try {
    Marshal.Copy(face,0,p,face.Length);atlasFont=CreateFontA(-16,0,0,0,700,0,0,0,1,0,0,4,2,p);
    if(atlasFont==IntPtr.Zero)throw new InvalidOperationException("actual atlas font failed");
    Marshal.Copy(new byte[60],0,p,60);int count=GetObjectA(atlasFont,60,p);byte[] b=new byte[60];Marshal.Copy(p,b,0,60);if(count!=60)throw new InvalidOperationException("actual atlas font description failed");
    atlasStep=5;return new {result=Pointer(atlasFont),inspection=new {native_requested=false,method="GetObjectA",result=count,hex=Hex(b)}};
   }finally{Marshal.FreeHGlobal(p);}
  }
  if(op=="atlas_bitmap_select" || op=="atlas_font_select") {
   Keys(r,"id","op","pointer","object");bool bitmap=op=="atlas_bitmap_select";IntPtr obj=bitmap?atlasBitmap:atlasFont;
   if(atlasStep!=(bitmap?5:6) || Number(r,"pointer")!=Pointer(atlasDC) || Number(r,"object")!=Pointer(obj))throw new ArgumentException("original atlas owned selection order");
   IntPtr old=SelectObject(atlasDC,obj);if(old==IntPtr.Zero || old.ToInt32()==-1)throw new InvalidOperationException("actual atlas selection failed");
   if(bitmap)atlasOldBitmap=old;else atlasOldFont=old;atlasStep++;return new {result=Pointer(old)};
  }
  if(op=="atlas_map" || op=="atlas_text" || op=="atlas_background" || op=="atlas_align") {
   Keys(r,"id","op","pointer","value");int step=op=="atlas_map"?2:op=="atlas_text"?7:op=="atlas_background"?8:9;
   uint value=Number(r,"value"),expected=op=="atlas_map"?1u:op=="atlas_text"?0xffffffu:0u;
   if(atlasStep!=step || Number(r,"pointer")!=Pointer(atlasDC) || value!=expected)throw new ArgumentException("original atlas owned DC state/order");
   uint result=op=="atlas_map"?(uint)SetMapMode(atlasDC,(int)value):op=="atlas_text"?SetTextColor(atlasDC,value):op=="atlas_background"?SetBkColor(atlasDC,value):SetTextAlign(atlasDC,value);
   if(result==uint.MaxValue || (op=="atlas_map" && result==0))throw new InvalidOperationException("actual atlas DC state failed");atlasStep++;return new {result=result};
  }
  if(op=="glyph_pixels") {
   Keys(r,"id","op","pointer","stage");string stage=(string)r["stage"];
   if(atlasStep!=10 || Number(r,"pointer")!=Pointer(atlasBits) || awaitingDraw ||
      (stage=="before"?(glyphIndex!=0 || snapshotMask!=0):(stage!="after" || glyphIndex!=95 || snapshotMask!=1)))throw new ArgumentException("bounded owned glyph snapshot order");
   if(!GdiFlush())throw new InvalidOperationException("actual GDI flush failed");byte[] b=new byte[262144];Marshal.Copy(atlasBits,b,0,b.Length);snapshotMask|=stage=="before"?1:2;
   return new {result=1,native_requested=false,method="GdiFlush/owned DIB snapshot",completed_glyphs=glyphIndex,hex=Hex(b)};
  }
  if(op=="glyph_measure") {
   Keys(r,"id","op","pointer","character","before_hex");uint ch=Number(r,"character");string before=(string)r["before_hex"];
   if(atlasStep!=10 || snapshotMask!=1 || awaitingDraw || glyphIndex>=95 || ch!=32+glyphIndex || Number(r,"pointer")!=Pointer(atlasDC) || before.Length!=16)throw new ArgumentException("original bounded glyph measurement order/owner");
   byte[] b=new byte[8];for(int i=0;i<8;i++)b[i]=Convert.ToByte(before.Substring(i*2,2),16);
   IntPtr text=Marshal.AllocHGlobal(1),output=Marshal.AllocHGlobal(8);try {
    Marshal.WriteByte(text,(byte)ch);Marshal.Copy(b,0,output,8);if(!GetTextExtentPoint32A(atlasDC,text,1,output))throw new InvalidOperationException("actual glyph measurement failed");
    Marshal.Copy(output,b,0,8);glyphWidth=BitConverter.ToInt32(b,0);glyphHeight=BitConverter.ToInt32(b,4);
    if(glyphWidth<=0 || glyphWidth>256 || glyphHeight<=0 || glyphHeight>256)throw new InvalidOperationException("actual glyph outside bounded atlas");
    if(penX+glyphWidth+1>256){penX=0;penY+=glyphHeight+1;}if(penY+glyphHeight>256)throw new InvalidOperationException("actual glyph atlas overflow");
    awaitingDraw=true;return new {result=1,hex=Hex(b)};
   }finally{Marshal.FreeHGlobal(text);Marshal.FreeHGlobal(output);}
  }
  if(op=="glyph_draw") {
   Keys(r,"id","op","pointer","character","x","y");uint ch=Number(r,"character");
   if(atlasStep!=10 || !awaitingDraw || ch!=32+glyphIndex || Number(r,"pointer")!=Pointer(atlasDC) || Number(r,"x")!=penX || Number(r,"y")!=penY)throw new ArgumentException("original bounded glyph draw order/position/owner");
   IntPtr text=Marshal.AllocHGlobal(1);try{Marshal.WriteByte(text,(byte)ch);if(!ExtTextOutA(atlasDC,penX,penY,2,IntPtr.Zero,text,1,IntPtr.Zero))throw new InvalidOperationException("actual glyph draw failed");}finally{Marshal.FreeHGlobal(text);}
   penX+=glyphWidth+1;glyphIndex++;awaitingDraw=false;return new {result=1};
  }
  if(op=="font_delete_bitmap") {
   Keys(r,"id","op","pointer");if(nativeCleanupStep!=0 || glyphIndex!=95 || snapshotMask!=3 || Number(r,"pointer")!=Pointer(atlasBitmap))throw new ArgumentException("original owned bitmap deletion order");
   bool result=DeleteObject(atlasBitmap);bitmapDeleteIssued=result;nativeCleanupStep=1;return new {result=result?1:0};
  }
  if(op=="font_delete_dc") {
   Keys(r,"id","op","pointer");if(nativeCleanupStep!=1 || Number(r,"pointer")!=Pointer(atlasDC))throw new ArgumentException("original owned DC deletion order");
   bool result=DeleteDC(atlasDC);if(result){atlasDC=IntPtr.Zero;atlasOldFont=IntPtr.Zero;atlasOldBitmap=IntPtr.Zero;nativeDCReleased++;}
   if(!GdiFlush())throw new InvalidOperationException("actual native deletion inspection flush failed");uint type=GetObjectType(atlasBitmap);int live=LiveBytes(atlasBitmap);if(bitmapDeleteIssued && live==0){nativeBitmapReleased++;atlasBitmap=IntPtr.Zero;atlasBits=IntPtr.Zero;}
   nativeCleanupStep=2;return new {result=result?1:0,inspection=new {native_requested=false,method="GdiFlush/GetObjectA/GetObjectType(bitmap)",result=live,reported_type=type}};
  }
  if(op=="font_delete_font") {
   Keys(r,"id","op","pointer");if(nativeCleanupStep!=2 || Number(r,"pointer")!=Pointer(atlasFont))throw new ArgumentException("original owned font deletion order");
   bool result=DeleteObject(atlasFont);fontDeleteIssued=result;if(result && atlasDC==IntPtr.Zero){atlasFont=IntPtr.Zero;nativeFontReleased++;}nativeCleanupStep=3;return new {result=result?1:0};
  }
  if(op=="close"){Keys(r,"id","op");return Cleanup();}
  throw new ArgumentException("unsupported owner platform operation");
 }
 static void Emit(object r){Console.WriteLine(json.Serialize(r));Console.Out.Flush();}
 static int Main() {
  try {
   if(IntPtr.Size!=4)throw new InvalidOperationException("x86 required");Emit(new {ok=true,id=0,hello=new {pointer_bytes=4,acp=GetACP()}});
   string line;while((line=Console.ReadLine())!=null) {
    long id=0;string op="";try {
     if(line.Length>8192)throw new ArgumentException("bounded request");var r=json.Deserialize<Dictionary<string,object>>(line);id=Number(r,"id");op=(string)r["op"];
     if(id!=sequence+1)throw new ArgumentException("sequence");sequence=id;
     object result=Dispatch(r);Emit(new {ok=true,id=id,result=result});if(op=="close")break;
    }catch(Exception e){Emit(new {ok=false,id=id,error=e.GetType().Name+": "+e.Message});}
   }return 0;
  }catch(Exception e){Emit(new {ok=false,id=0,error=e.GetType().Name+": "+e.Message});return 2;}
  finally{Cleanup();}
 }
}
