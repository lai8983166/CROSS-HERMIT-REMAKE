
undefined4 FUN__text__0052ab47(char *param_1,int param_2,int param_3)

{
  int iVar1;
  char *pcVar2;
  
  if (param_2 == 0) {
    return 0;
  }
  if (param_3 == 0) {
    return 0;
  }
  if ((int)param_1 < -0x7789f799) {
    if (param_1 == (char *)0x88760866) {
      param_1 = "D3DERR_NOTFOUND";
    }
    else if ((int)param_1 < -0x7789f7e3) {
      if (param_1 == (char *)0x8876081c) {
        param_1 = "D3DERR_UNSUPPORTEDALPHAARG";
      }
      else if ((int)param_1 < -0x7789f7e7) {
        if (param_1 == (char *)0x88760818) {
          param_1 = "D3DERR_WRONGTEXTUREFORMAT";
        }
        else if (param_1 == (char *)0x80004001) {
          param_1 = "E_NOTIMPL";
        }
        else if (param_1 == (char *)0x80004005) {
          param_1 = "E_FAIL";
        }
        else if (param_1 == (char *)0x8007000e) {
          param_1 = "E_OUTOFMEMORY";
        }
        else {
          if (param_1 != (char *)0x8876017c) goto LAB__text__0052ad92;
          param_1 = "D3DERR_OUTOFVIDEOMEMORY";
        }
      }
      else if (param_1 == (char *)0x88760819) {
        param_1 = "D3DERR_UNSUPPORTEDCOLOROPERATION";
      }
      else if (param_1 == (char *)0x8876081a) {
        param_1 = "D3DERR_UNSUPPORTEDCOLORARG";
      }
      else {
        if (param_1 != (char *)0x8876081b) {
LAB__text__0052ad92:
          pcVar2 = "Unrecognized error: 0x%0.8x";
          goto LAB__text__0052ad98;
        }
        param_1 = "D3DERR_UNSUPPORTEDALPHAOPERATION";
      }
    }
    else if (param_1 == (char *)0x8876081d) {
      param_1 = "D3DERR_TOOMANYOPERATIONS";
    }
    else if (param_1 == (char *)0x8876081e) {
      param_1 = "D3DERR_CONFLICTINGTEXTUREFILTER";
    }
    else if (param_1 == (char *)0x8876081f) {
      param_1 = "D3DERR_UNSUPPORTEDFACTORVALUE";
    }
    else if (param_1 == (char *)0x88760821) {
      param_1 = "D3DERR_CONFLICTINGRENDERSTATE";
    }
    else if (param_1 == (char *)0x88760822) {
      param_1 = "D3DERR_UNSUPPORTEDTEXTUREFILTER";
    }
    else if (param_1 == (char *)0x88760826) {
      param_1 = "D3DERR_CONFLICTINGTEXTUREPALETTE";
    }
    else {
      if (param_1 != (char *)0x88760827) goto LAB__text__0052ad92;
      param_1 = "D3DERR_DRIVERINTERNALERROR";
    }
  }
  else if ((int)param_1 < -0x7789f4ab) {
    if (param_1 == (char *)0x88760b54) {
      param_1 = "D3DXERR_CANNOTMODIFYINDEXBUFFER";
    }
    else if (param_1 == (char *)0x88760867) {
      param_1 = "D3DERR_MOREDATA";
    }
    else if (param_1 == (char *)0x88760868) {
      param_1 = "D3DERR_DEVICELOST";
    }
    else if (param_1 == (char *)0x88760869) {
      param_1 = "D3DERR_DEVICENOTRESET";
    }
    else if (param_1 == (char *)0x8876086a) {
      param_1 = "D3DERR_NOTAVAILABLE";
    }
    else if (param_1 == (char *)0x8876086b) {
      param_1 = "D3DERR_INVALIDDEVICE";
    }
    else if (param_1 == (char *)0x8876086c) {
      param_1 = "D3DERR_INVALIDCALL";
    }
    else {
      if (param_1 != (char *)0x8876086d) goto LAB__text__0052ad92;
      param_1 = "D3DERR_DRIVERINVALIDCALL";
    }
  }
  else if (param_1 == (char *)0x88760b55) {
    param_1 = "D3DXERR_INVALIDMESH";
  }
  else if (param_1 == (char *)0x88760b56) {
    param_1 = "D3DXERR_CANNOTATTRSORT";
  }
  else if (param_1 == (char *)0x88760b57) {
    param_1 = "D3DXERR_SKINNINGNOTSUPPORTED";
  }
  else if (param_1 == (char *)0x88760b58) {
    param_1 = "D3DXERR_TOOMANYINFLUENCES";
  }
  else if (param_1 == (char *)0x88760b59) {
    param_1 = "D3DXERR_INVALIDDATA";
  }
  else if (param_1 == (char *)0x88760b5a) {
    param_1 = "D3DXERR_LOADEDMESHASNODATA";
  }
  else {
    if (param_1 != (char *)0x0) goto LAB__text__0052ad92;
    param_1 = "S_OK";
  }
  pcVar2 = "%s";
LAB__text__0052ad98:
  iVar1 = FUN__text__005715b0(param_2,param_3,pcVar2,param_1);
  if ((iVar1 < 0) && (param_3 != 0)) {
    *(undefined1 *)(param_2 + -1 + param_3) = 0;
  }
  return 0;
}

