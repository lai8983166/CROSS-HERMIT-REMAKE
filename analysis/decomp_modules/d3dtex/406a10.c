
void __fastcall FUN__text__00406a10(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  void *local_1c;
  void *local_18;
  void *local_14;
  undefined1 local_10 [8];
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(int *)(param_1 + 0x2c) != 0) &&
     (local_8 = param_1,
     local_18 = (void *)FUN__text__00428a40((int)*(short *)(param_1 + 0x3c) << 2),
     local_14 = local_18, local_18 != (void *)0x0)) {
    _memset(local_18,0,(int)*(short *)(local_8 + 0x3c) << 2);
    FUN__text__0056d810(local_14,"ADDR=%08x , w:%4d(%4d) , h:%4d(%4d)\n",
                        *(undefined4 *)(local_8 + 0x2c),(int)*(short *)(local_8 + 0x38),
                        (int)*(short *)(local_8 + 0x3c),(int)*(short *)(local_8 + 0x3a),
                        (int)*(short *)(local_8 + 0x3e));
    (*API_KERNEL32_DLL_OutputDebugStringA)(local_14);
    FUN__text__0056ce80();
    iVar1 = FUN__text__00403910(local_10);
    if (iVar1 == 0) {
      local_20 = FUN__text__004037f0();
      if (local_20 == 8) {
        FUN__text__00406b70(local_10,local_14);
      }
      else if (local_20 == 0x10) {
        FUN__text__00406ca0(local_10,local_14);
      }
      else {
        (*API_KERNEL32_DLL_OutputDebugStringA)("DebugTextureOutput():DONT DISP TEX-MODE\n");
        FUN__text__0056ce80();
      }
      iVar1 = FUN__text__00403990();
      if (iVar1 == 0) {
        local_1c = local_14;
        FUN__text__00428ad0(local_14);
      }
    }
  }
  local_8 = 0x406b6b;
  FUN__text__0056ce80();
  return;
}

