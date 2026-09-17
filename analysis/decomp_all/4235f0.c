
void __thiscall
FUN__text__004235f0(undefined4 *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                   undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_88 [16];
  undefined4 local_48;
  undefined4 local_44;
  code *local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined *local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  uint local_24;
  char *local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 *local_8;
  
  puVar3 = local_88;
  for (iVar2 = 0x21; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  (*API_USER32_DLL_SetRect)(param_1 + 6,param_2,param_3,param_4,param_5);
  FUN__text__0056ce80();
  local_18 = local_8[6];
  local_14 = local_8[7];
  local_10 = local_8[8];
  local_c = local_8[9];
  (*API_USER32_DLL_AdjustWindowRect)(&local_18,param_6,1);
  FUN__text__0056ce80();
  local_48 = 0x30;
  local_44 = 0;
  local_20 = "Cross Hermit";
  local_40 = FUN__text__0049e850;
  local_34 = PTR_IMAGE_DOS_HEADER_007a2728;
  local_3c = 0;
  local_38 = 0;
  (*API_USER32_DLL_LoadIconA)(PTR_IMAGE_DOS_HEADER_007a2728,*(undefined2 *)(local_8 + 10));
  local_30 = FUN__text__0056ce80();
  (*API_USER32_DLL_LoadIconA)(PTR_IMAGE_DOS_HEADER_007a2728,*(undefined2 *)(local_8 + 10));
  local_1c = FUN__text__0056ce80();
  (*API_USER32_DLL_LoadCursorA)(0,0x7f00);
  local_2c = FUN__text__0056ce80();
  local_28 = 0;
  local_24 = (uint)*(ushort *)(local_8 + 0xb);
  (*API_USER32_DLL_RegisterClassExA)(&local_48);
  sVar1 = FUN__text__0056ce80();
  if (sVar1 != 0) {
    (*API_USER32_DLL_CreateWindowExA)
              (0,"Cross Hermit","Cross Hermit",param_6,local_18,local_14,local_10,local_c,0,0,
               PTR_IMAGE_DOS_HEADER_007a2728,0);
    PTR_DAT_007a0bb4 = (undefined *)FUN__text__0056ce80();
    if (PTR_DAT_007a0bb4 != (undefined *)0x0) {
      (*API_USER32_DLL_ShowWindow)(PTR_DAT_007a0bb4,param_7);
      FUN__text__0056ce80();
      (*API_USER32_DLL_UpdateWindow)(PTR_DAT_007a0bb4);
      FUN__text__0056ce80();
      *local_8 = 1;
      FUN__text__00423800(PTR_DAT_007a0bb4);
    }
  }
  local_44 = 0x4237ee;
  FUN__text__0056ce80();
  return;
}

