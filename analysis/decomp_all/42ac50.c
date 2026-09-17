
void FUN__text__0042ac50(undefined4 param_1,int param_2,int param_3,int *param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [10];
  undefined4 uStack_2c;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  (*API_KERNEL32_DLL_GetCurrentDirectoryA)
            (0x104,"F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\data\\Tactics\\Title.bin");
  FUN__text__0056ce80();
  (*DAT_005921ec)(param_1,0x80000000,1,0,3,1,0);
  local_8 = FUN__text__0056ce80();
  FUN__text__0056d810("F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\data\\Tactics\\Title.bin",
                      &DAT_00592a18,param_1);
  if ((local_8 == -1) &&
     (iVar2 = FUN__text__00424f80(&DAT_00595040,"E:\\CrossHermit\\GAME\\src\\system\\System.cpp",
                                  DAT_005ff718 + 0x14,
                                  "F:\\project\\chaomofa\\CROSS HERMIT\\CROSS HERMIT\\data\\Tactics\\Title.bin"
                                 ), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_8 != -1) {
    (*DAT_005921f0)(local_8,0);
    local_c = FUN__text__0056ce80();
    if (local_c != -1) {
      if (param_4 != (int *)0x0) {
        *param_4 = local_c;
      }
      if ((param_3 != 1) ||
         (param_2 = FUN__text__00428a40(local_c), local_14 = param_2, param_2 != 0)) {
        (*DAT_005921e8)(local_8,param_2,local_c,&local_10,0);
        iVar2 = FUN__text__0056ce80();
        if ((iVar2 != 0) && (local_c == local_10)) {
          (*DAT_00592270)(local_8);
          FUN__text__0056ce80();
          goto LAB__text__0042adbd;
        }
      }
    }
    (*DAT_00592270)(local_8);
    FUN__text__0056ce80();
  }
LAB__text__0042adbd:
  uStack_2c = 0x42adca;
  FUN__text__0056ce80();
  return;
}

