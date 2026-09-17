
void __thiscall
FUN__text__0047fcf0(int param_1,int param_2,undefined2 param_3,undefined2 param_4,undefined4 param_5
                   )

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  short local_18 [2];
  short local_14 [2];
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (((param_2 < 0) || (0xf9 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=unit_workno)&&(unit_workno<(250))",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e8c + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_1c = local_8 + 0x80aec + param_2 * 0x520;
  iVar2 = FUN__text__00468d80(local_1c);
  local_10 = (uint)(iVar2 != 0);
  iVar2 = FUN__text__00468d10(local_1c);
  if ((iVar2 == 0) || (iVar2 = FUN__text__0046a120(local_1c), iVar2 == 0)) {
    iVar2 = FUN__text__00424f80(&DAT_0059d698,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e8c + 0xc,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    FUN__text__0043d4e0();
    local_c = 0;
    iVar2 = FUN__text__00468d10(local_1c);
    if (((iVar2 != 0) && (iVar2 = FUN__text__0046a120(local_1c), iVar2 != 0)) &&
       (iVar2 = FUN__text__0043d660(param_3,CONCAT22((short)((uint)*(int *)(local_1c + 600) >> 0x10)
                                                     ,param_4),param_5,
                                    *(undefined1 *)(*(int *)(local_1c + 600) + 0x30),local_14,
                                    local_18), iVar2 != 0)) {
      FUN__text__00480040(local_10,local_1c,(int)local_14[0],(int)local_18[0]);
      local_c = local_c + 1;
    }
  }
  local_8 = 0x47fe69;
  FUN__text__0056ce80();
  return;
}

