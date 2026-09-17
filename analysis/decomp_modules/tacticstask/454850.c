
void FUN__text__00454850(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (DAT_007a49fc != 0) {
    uVar1 = FUN__text__00429720();
    (*API_KERNEL32_DLL_lstrcpyA)(&DAT_007a4070,uVar1);
    FUN__text__0056ce80();
    (*API_KERNEL32_DLL_lstrcatA)(&DAT_007a4070,(&PTR_s_data_sound_bgm_M_001_mp3_0060ca2c)[param_1]);
    FUN__text__0056ce80();
    FUN__text__0041e190(&DAT_007a4070,1);
  }
  local_8 = 0x4548d6;
  FUN__text__0056ce80();
  return;
}

