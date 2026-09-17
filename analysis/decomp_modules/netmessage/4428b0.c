
void FUN__text__004428b0(undefined4 param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0041abf0(param_1);
  if (local_c == 0) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                DAT_005ffc90 + 7,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *(undefined1 *)(local_c + 1) = 0;
    local_10 = FUN__text__00442b30();
  }
  local_8 = 0x44293e;
  FUN__text__0056ce80();
  return;
}

