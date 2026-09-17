
void __thiscall FUN__text__00425cc0(undefined4 *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [15];
  undefined4 uStack_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  uint local_c;
  undefined4 *local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  local_18 = FUN__text__0056cd3e(*param_1);
  if ((local_18 == 0) &&
     (iVar2 = FUN__text__00424f80("hwnd!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                  DAT_005ff678 + 0xb,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_1c = FUN__text__0056cd38(local_18);
  if ((local_1c == 0) &&
     (iVar2 = FUN__text__00424f80("himc!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                  DAT_005ff678 + 0xe,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (uint)(param_2 != 0);
  local_10 = FUN__text__0056cd50(local_1c,local_c);
  if (local_10 == 0) {
    FUN__text__004295c0();
  }
  local_14 = FUN__text__0056cd2c(local_18,local_1c);
  if ((local_14 == 0) &&
     (iVar2 = FUN__text__00424f80("ret!=0","e:\\crosshermit\\game\\src\\system\\sysime.cpp",
                                  DAT_005ff678 + 0x17,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  uStack_20 = 0x425dd2;
  FUN__text__0056ce80();
  return;
}

