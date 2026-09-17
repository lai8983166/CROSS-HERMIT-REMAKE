
void __fastcall FUN__text__00482150(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  char local_10;
  char *local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x115cac);
  local_8 = param_1;
  iVar2 = FUN__text__00481b90();
  if (iVar2 != 0) {
    local_10 = *local_c;
    if (local_10 == '\0') {
      FUN__text__00482210(local_c);
    }
    else if (local_10 == '\x01') {
      FUN__text__00482370(local_c);
    }
    else if (local_10 == '\x02') {
      FUN__text__004824a0(local_c);
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                  DAT_00618ee4 + 6,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  local_8 = 0x482204;
  FUN__text__0056ce80();
  return;
}

