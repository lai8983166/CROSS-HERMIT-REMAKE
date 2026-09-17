
void FUN__text__00437560(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_150 [16];
  undefined1 local_110 [228];
  undefined4 uStack_2c;
  undefined4 local_10;
  int local_c;
  
  puVar2 = local_150;
  for (iVar1 = 0x53; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  (*DAT_00592354)(param_1,0x9f,param_2,FUN__text__004376b0,0);
  local_10 = FUN__text__0056ce80();
  local_c = (uint)DAT_007a2944 * 0x1000000 + (uint)DAT_007a2945 * 0x10000 +
            (uint)DAT_007a2946 * 0x100 + (uint)DAT_007a2947;
  FUN__text__0056d810(local_110,&DAT_005953b0,DAT_007a2944,DAT_007a2945,DAT_007a2946,DAT_007a2947);
  (*DAT_005923d8)(param_2,local_110,&DAT_005953ac,0);
  FUN__text__0056ce80();
  uStack_2c = 0x437643;
  FUN__text__0056ce80();
  return;
}

