
void __fastcall FUN__text__00425ac0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0xc) == 0) &&
     (iVar2 = FUN__text__00424f80("SyshKl!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                  DAT_005ff674 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN__text__00425c10();
  local_10 = FUN__text__0056cd44(*(undefined4 *)(local_8 + 0xc),0,0);
  if ((local_10 == 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_00594b44,"e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                  DAT_005ff674 + 8,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_10 != 0) {
    local_14 = FUN__text__00428a40(local_10 + 2);
    *(undefined4 *)(local_8 + 0x10) = local_14;
    if ((*(int *)(local_8 + 0x10) == 0) &&
       (iVar2 = FUN__text__00424f80("SysImeName != 0",
                                    "e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                    DAT_005ff674 + 0xc,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (((*(int *)(local_8 + 0x10) != 0) &&
        (local_c = FUN__text__0056cd44(*(undefined4 *)(local_8 + 0xc),
                                       *(undefined4 *)(local_8 + 0x10),local_10), local_c == 0)) &&
       (iVar2 = FUN__text__00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                    DAT_005ff674 + 0x10,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_14 = 0x425c0a;
  FUN__text__0056ce80();
  return;
}

