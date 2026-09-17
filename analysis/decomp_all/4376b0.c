
void FUN__text__004376b0(undefined4 param_1,uint param_2,uint param_3,int *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_258 [16];
  int local_218;
  uint local_214;
  uint local_210;
  undefined1 local_20c [512];
  int local_c;
  int *local_8;
  
  puVar2 = local_258;
  for (iVar1 = 0x95; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_210 = param_2;
  if (param_2 < 0x4f) {
    if ((param_2 == 0x4e) && (*param_4 == DAT_007a2940)) {
      local_8 = param_4;
      local_218 = param_4[2];
      if (local_218 == -0x35c) {
        (&DAT_007a2944)[param_4[3]] = (char)param_4[4];
        (*API_USER32_DLL_wsprintfA)
                  (local_20c,"1st = %d, 2nd = %d, 3rd = %d, 4th = %d",DAT_007a2944,DAT_007a2945,
                   DAT_007a2946,DAT_007a2947);
        FUN__text__0056ce80();
      }
    }
  }
  else if (param_2 == 0x110) {
    (*API_USER32_DLL_GetDlgItem)(param_1,0x462);
    DAT_007a2940 = FUN__text__0056ce80();
    local_c = (uint)DAT_007a2944 * 0x1000000 + (uint)DAT_007a2945 * 0x10000 +
              (uint)DAT_007a2946 * 0x100 + (uint)DAT_007a2947;
    (*API_USER32_DLL_SendMessageA)(DAT_007a2940,0x465,0,local_c);
    FUN__text__0056ce80();
    (*API_USER32_DLL_SetFocus)(DAT_007a2940);
    FUN__text__0056ce80();
  }
  else if (((param_2 == 0x111) && (local_214 = param_3 & 0xffff, local_214 != 0)) && (local_214 < 3)
          ) {
    (*DAT_005923c4)(param_1,1);
    FUN__text__0056ce80();
  }
  local_8 = (int *)0x4378c4;
  FUN__text__0056ce80();
  return;
}

