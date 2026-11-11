// Independent presented-frame capture. No PrintWindow, hooks or game writes.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <d3d11.h>
#include <dxgi1_2.h>
#include <dwmapi.h>
#include <wrl/client.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <sstream>
using Microsoft::WRL::ComPtr;
static int patternSeed=0;
static void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
static void hr(HRESULT h,const char* s){if(FAILED(h)){std::ostringstream o;o<<s<<":0x"<<std::hex<<(unsigned)h;throw std::runtime_error(o.str());}}
static LONGLONG tick(){LARGE_INTEGER n;QueryPerformanceCounter(&n);return n.QuadPart;}
static COLORREF color(int x,int y,int seed){
    const COLORREF p[]={RGB(255,0,0),RGB(0,255,0),RGB(0,0,255),RGB(255,255,0),
                        RGB(255,0,255),RGB(0,255,255),RGB(0,0,0),RGB(255,255,255)};
    return p[((x/32)+3*(y/32)+seed)%8];
}
static LRESULT CALLBACK proc(HWND w,UINT m,WPARAM a,LPARAM b){
    if(m==WM_PAINT){PAINTSTRUCT ps;HDC dc=BeginPaint(w,&ps);
        for(int y=0;y<192;y+=32)for(int x=0;x<256;x+=32){RECT r{x,y,x+32,y+32};
            HBRUSH brush=CreateSolidBrush(color(x,y,patternSeed));FillRect(dc,&r,brush);DeleteObject(brush);}
        EndPaint(w,&ps);return 0;}
    return DefWindowProcW(w,m,a,b);
}
static RECT bounds(HWND w,DWORD pid){
    DWORD actual=0;GetWindowThreadProcessId(w,&actual);
    need(IsWindow(w)&&actual==pid&&GetForegroundWindow()==w&&IsWindowVisible(w)&&!IsIconic(w),"window identity/foreground");
    RECT r;need(GetClientRect(w,&r)!=0,"client rectangle");POINT a{r.left,r.top},b{r.right,r.bottom};
    need(ClientToScreen(w,&a)&&ClientToScreen(w,&b),"client screen mapping");
    need(b.x-a.x>=64&&b.y-a.y>=64&&(long long)(b.x-a.x)*(b.y-a.y)<=4096LL*2160,"bounded capture area");
    RECT target{a.x,a.y,b.x,b.y};int inspected=0;
    for(HWND above=GetWindow(w,GW_HWNDPREV);above;above=GetWindow(above,GW_HWNDPREV)){
        need(++inspected<4096,"bounded occlusion check");if(!IsWindowVisible(above)||IsIconic(above))continue;
        DWORD cloaked=0;DwmGetWindowAttribute(above,DWMWA_CLOAKED,&cloaked,sizeof(cloaked));if(cloaked)continue;
        RECT other,overlap;if(GetWindowRect(above,&other)&&IntersectRect(&overlap,&target,&other))
            throw std::runtime_error("target covered by another window");
    }
    return target;
}
struct Frame{int width,height;LONGLONG requested,present;UINT accumulated;UINT skipped;size_t firstMismatch;std::vector<unsigned char> pixels;};
static Frame capture(HWND w,DWORD pid,LONGLONG after,int seed=0){
    RECT r=bounds(w,pid);HMONITOR mon=MonitorFromWindow(w,MONITOR_DEFAULTTONULL);need(mon!=nullptr,"target monitor");
    ComPtr<IDXGIFactory1> factory;hr(CreateDXGIFactory1(IID_PPV_ARGS(&factory)),"factory");
    ComPtr<IDXGIAdapter1> adapter;ComPtr<IDXGIOutput> output;DXGI_OUTPUT_DESC od{};bool found=false;
    for(UINT ai=0;!found;ai++){
        ComPtr<IDXGIAdapter1> a;HRESULT ah=factory->EnumAdapters1(ai,&a);if(ah==DXGI_ERROR_NOT_FOUND)break;hr(ah,"adapter");
        for(UINT oi=0;;oi++){ComPtr<IDXGIOutput> o;HRESULT oh=a->EnumOutputs(oi,&o);if(oh==DXGI_ERROR_NOT_FOUND)break;hr(oh,"output");
            DXGI_OUTPUT_DESC d;hr(o->GetDesc(&d),"output description");if(d.Monitor==mon){adapter=a;output=o;od=d;found=true;break;}}
    }
    need(found,"monitor has no DXGI output");need(od.Rotation==DXGI_MODE_ROTATION_IDENTITY,"rotated output not qualified");
    RECT d=od.DesktopCoordinates;need(r.left>=d.left&&r.top>=d.top&&r.right<=d.right&&r.bottom<=d.bottom,"window spans output");
    ComPtr<ID3D11Device> device;ComPtr<ID3D11DeviceContext> context;D3D_FEATURE_LEVEL level;
    hr(D3D11CreateDevice(adapter.Get(),D3D_DRIVER_TYPE_UNKNOWN,nullptr,0,nullptr,0,D3D11_SDK_VERSION,&device,&level,&context),"device");
    ComPtr<IDXGIOutput1> o1;hr(output.As(&o1),"output1");ComPtr<IDXGIOutputDuplication> dup;
    hr(o1->DuplicateOutput(device.Get(),&dup),"duplicate output");
    if(seed){patternSeed=seed;after=tick();InvalidateRect(w,nullptr,FALSE);UpdateWindow(w);hr(DwmFlush(),"pattern present");}
    struct Release{IDXGIOutputDuplication* p;bool held=false;~Release(){if(held)p->ReleaseFrame();}} release{dup.Get()};
    ULONGLONG end=GetTickCount64()+5000;UINT skipped=0;size_t firstMismatch=0;
    for(;;){
    ComPtr<IDXGIResource> resource;DXGI_OUTDUPL_FRAME_INFO info{};
    while(true){
        HRESULT h=dup->AcquireNextFrame(100,&info,&resource);
        if(h==DXGI_ERROR_WAIT_TIMEOUT){need(GetTickCount64()<end,"fresh frame timeout");continue;}hr(h,"acquire frame");release.held=true;
        need(!info.ProtectedContentMaskedOut,"protected content masked");
        if(info.LastPresentTime.QuadPart>after&&info.AccumulatedFrames>0)break;
        resource.Reset();hr(dup->ReleaseFrame(),"release stale/mouse-only frame");release.held=false;
        need(GetTickCount64()<end,"no presented frame after request");
    }
    RECT check=bounds(w,pid);need(EqualRect(&check,&r)!=0,"window moved during capture");
    ComPtr<ID3D11Texture2D> source;hr(resource.As(&source),"frame texture");D3D11_TEXTURE2D_DESC sd;source->GetDesc(&sd);
    need(sd.Format==DXGI_FORMAT_B8G8R8A8_UNORM,"BGRA frame required");
    int width=r.right-r.left,height=r.bottom-r.top;D3D11_TEXTURE2D_DESC td{};
    td.Width=width;td.Height=height;td.MipLevels=1;td.ArraySize=1;td.Format=sd.Format;td.SampleDesc.Count=1;
    td.Usage=D3D11_USAGE_STAGING;td.CPUAccessFlags=D3D11_CPU_ACCESS_READ;
    ComPtr<ID3D11Texture2D> crop;hr(device->CreateTexture2D(&td,nullptr,&crop),"crop staging texture");
    D3D11_BOX box{(UINT)(r.left-d.left),(UINT)(r.top-d.top),0,(UINT)(r.right-d.left),(UINT)(r.bottom-d.top),1};
    need(box.right<=sd.Width&&box.bottom<=sd.Height,"crop within frame");
    context->CopySubresourceRegion(crop.Get(),0,0,0,0,source.Get(),0,&box);
    D3D11_MAPPED_SUBRESOURCE mapped;hr(context->Map(crop.Get(),0,D3D11_MAP_READ,0,&mapped),"map crop");
    Frame f{width,height,after,info.LastPresentTime.QuadPart,info.AccumulatedFrames,0,0,std::vector<unsigned char>((size_t)width*height*4)};
    for(int y=0;y<height;y++)memcpy(f.pixels.data()+(size_t)y*width*4,(char*)mapped.pData+(size_t)y*mapped.RowPitch,(size_t)width*4);
    context->Unmap(crop.Get(),0);hr(dup->ReleaseFrame(),"release frame");release.held=false;
    // A fresh desktop timestamp may still precede the popup's actual content.
    // Readiness is independently known for our test pattern; never persist a
    // mismatching crop (it could contain the previous background).
    if(seed){size_t mismatch=0;
        for(int y=0;y<f.height;y++)for(int x=0;x<f.width;x++){auto c=color(x,y,seed);size_t i=((size_t)y*f.width+x)*4;
            if(f.pixels[i]!=GetBValue(c)||f.pixels[i+1]!=GetGValue(c)||f.pixels[i+2]!=GetRValue(c))mismatch++;}
        if(mismatch){if(skipped==0)firstMismatch=mismatch;skipped++;
            need(GetTickCount64()<end,"target pattern not presented within capture budget");continue;}
    }
    f.skipped=skipped;f.firstMismatch=firstMismatch;
    context->ClearState();context->Flush();return f;
    }
}
static void save(const Frame& f,const std::wstring& path){
    BITMAPFILEHEADER fh{};BITMAPINFOHEADER ih{};fh.bfType=0x4D42;fh.bfOffBits=sizeof(fh)+sizeof(ih);fh.bfSize=fh.bfOffBits+(DWORD)f.pixels.size();
    ih.biSize=sizeof(ih);ih.biWidth=f.width;ih.biHeight=-f.height;ih.biPlanes=1;ih.biBitCount=32;ih.biSizeImage=(DWORD)f.pixels.size();
    HANDLE h=CreateFileW(path.c_str(),GENERIC_WRITE,0,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);need(h!=INVALID_HANDLE_VALUE,"fresh crop file");
    DWORD n=0;bool ok=WriteFile(h,&fh,sizeof(fh),&n,nullptr)&&n==sizeof(fh)&&WriteFile(h,&ih,sizeof(ih),&n,nullptr)&&n==sizeof(ih)
        &&WriteFile(h,f.pixels.data(),(DWORD)f.pixels.size(),&n,nullptr)&&n==f.pixels.size();CloseHandle(h);need(ok,"write crop");
}
int wmain(int argc,wchar_t** argv){
    HWND owned=nullptr,previous=GetForegroundWindow();DWORD previousPid=0;GetWindowThreadProcessId(previous,&previousPid);
    try{
        need(SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)!=0,"per-monitor DPI context");
        if(argc==3&&std::wstring(argv[1])==L"--selftest"){
            WNDCLASSW wc{};wc.lpfnWndProc=proc;wc.hInstance=GetModuleHandleW(nullptr);wc.lpszClassName=L"ChaomofaFrameQualification";
            need(RegisterClassW(&wc)!=0,"test window class");
            owned=CreateWindowExW(0,wc.lpszClassName,L"Frame capture qualification",WS_POPUP,80,80,256,192,nullptr,nullptr,wc.hInstance,nullptr);
            need(owned!=nullptr,"test window");ShowWindow(owned,SW_SHOWNORMAL);SetForegroundWindow(owned);
            std::cout<<"{\"frames\":[";
            for(int seed=1;seed<=2;seed++){
                Frame f=capture(owned,GetCurrentProcessId(),tick(),seed);size_t mismatch=0;
                for(int y=0;y<f.height;y++)for(int x=0;x<f.width;x++){COLORREF c=color(x,y,seed);size_t i=((size_t)y*f.width+x)*4;
                    if(f.pixels[i]!=GetBValue(c)||f.pixels[i+1]!=GetGValue(c)||f.pixels[i+2]!=GetRValue(c))mismatch++;}
                std::wstring path=std::wstring(argv[2])+L"/pattern-"+std::to_wstring(seed)+L".bmp";save(f,path);
                if(seed>1)std::cout<<",";
                std::cout<<"{\"seed\":"<<seed<<",\"mismatched_pixels\":"<<mismatch<<",\"request_qpc\":"<<f.requested
                         <<",\"present_qpc\":"<<f.present<<",\"accumulated_frames\":"<<f.accumulated<<",\"unready_frames_discarded\":"<<f.skipped<<",\"first_unready_mismatches\":"<<f.firstMismatch<<"}";
                need(mismatch==0,"pattern pixel mismatch");
            }
            DestroyWindow(owned);owned=nullptr;UnregisterClassW(wc.lpszClassName,wc.hInstance);
            DWORD nowPid=0;GetWindowThreadProcessId(previous,&nowPid);if(IsWindow(previous)&&previousPid==nowPid)SetForegroundWindow(previous);
            std::cout<<"],\"owned_window_destroyed\":true,\"all_capture_scopes_released\":true,\"accepted\":false}"<<std::endl;
        }else if(argc==7&&std::wstring(argv[1])==L"--window"){
            HWND w=(HWND)(uintptr_t)std::stoull(argv[2]);DWORD pid=std::stoul(argv[3]);auto main=(HANDLE)(uintptr_t)std::stoull(argv[4]);
            HANDLE process=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,pid);need(process!=nullptr,"target process");
            wchar_t path[32768];DWORD n=32768;BOOL ok=QueryFullProcessImageNameW(process,0,path,&n);CloseHandle(process);
            need(ok&&_wcsicmp(path,argv[5])==0&&GetPropA(w,"CPP_CLASS")==main,"target executable/property");
            Frame f=capture(w,pid,tick());need(GetPropA(w,"CPP_CLASS")==main,"target property changed");save(f,argv[6]);
            std::cout<<"{\"width\":"<<f.width<<",\"height\":"<<f.height<<",\"present_qpc\":"<<f.present
                     <<",\"accumulated_frames\":"<<f.accumulated<<",\"all_capture_scopes_released\":true,\"accepted\":false}"<<std::endl;
        }else throw std::runtime_error("explicit --selftest directory or --window hwnd pid main image crop required");
        return 0;
    }catch(const std::exception& e){if(owned)DestroyWindow(owned);DWORD p=0;GetWindowThreadProcessId(previous,&p);
        if(IsWindow(previous)&&p==previousPid)SetForegroundWindow(previous);
        std::cerr<<e.what()<<std::endl;return 1;}
}
