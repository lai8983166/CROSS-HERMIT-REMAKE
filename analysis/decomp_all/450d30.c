
void FUN__text__00450d30(undefined4 param_1,uint param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_a4 [16];
  uint local_64;
  int local_60;
  undefined1 local_5c [16];
  undefined1 local_4c [64];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_a4;
  for (iVar1 = 0x28; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((param_2 == 0x100) && (param_3 == 0xd)) {
    DAT_0079fc68 = 1;
  }
  local_60 = FUN__text__004272e0(param_1,param_2,param_3,param_4);
  if (local_60 != -1) goto LAB__text__00451036;
  local_64 = param_2;
  if (param_2 < 0x1d) {
    if (param_2 == 0x1c) {
      *(int *)(local_8 + 0x8d0) = param_3;
      if (DAT_007a49fc != 0) {
        FUN__text__00413e50(*(undefined4 *)(local_8 + 0x8d0));
        FUN__text__00412a70(*(undefined4 *)(local_8 + 0x8d0));
        FUN__text__0041d7f0(*(undefined4 *)(local_8 + 0x8d0));
        FUN__text__0041d7f0(*(undefined4 *)(local_8 + 0x8d0));
        FUN__text__0041d7f0(*(undefined4 *)(local_8 + 0x8d0));
      }
      goto LAB__text__00451036;
    }
    local_64 = param_2 - 1;
    switch(param_2) {
    case 1:
      break;
    case 2:
      (*API_USER32_DLL_PostQuitMessage)(0);
      FUN__text__0056ce80();
      break;
    default:
      goto switchD__text__00450dcf_caseD_3;
    case 5:
      break;
    case 0xf:
      (*API_USER32_DLL_BeginPaint)(param_1,local_4c);
      local_c = FUN__text__0056ce80();
      (*API_USER32_DLL_GetClientRect)(param_1,local_5c);
      FUN__text__0056ce80();
      (*API_USER32_DLL_EndPaint)(param_1,local_4c);
      FUN__text__0056ce80();
      break;
    case 0x10:
      (*API_USER32_DLL_DestroyWindow)(param_1);
      FUN__text__0056ce80();
      break;
    case 0x12:
    }
  }
  else {
    if (param_2 < 0x201) {
      if (param_2 == 0x200) {
        if (DAT_007a49fc != 0) {
          FUN__text__00412b40(param_1,0x200,param_3,param_4);
        }
        goto LAB__text__00451036;
      }
      if (((param_2 == 0x4e) || (param_2 == 0x111)) ||
         ((param_2 == 0x112 && (((param_3 == 0xf030 || (param_3 == 0xf100)) || (param_3 == 0xf140)))
          ))) goto LAB__text__00451036;
    }
    else {
      if (param_2 == 0x233) goto LAB__text__00451036;
      if (param_2 == 0x464) {
        if (DAT_007a49fc != 0) {
          if (param_4 == DAT_007a49fc + 0x8c88) {
            FUN__text__0041e940();
          }
          if (param_4 == DAT_007a49fc + 0x8f00) {
            FUN__text__0041e940();
          }
        }
        goto LAB__text__00451036;
      }
    }
switchD__text__00450dcf_caseD_3:
    FUN__text__00424a90(param_1,param_2,param_3,param_4);
  }
LAB__text__00451036:
  local_8 = 0x451046;
  FUN__text__0056ce80();
  return;
}

