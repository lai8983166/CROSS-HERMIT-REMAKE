
void FUN__text__00443080(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1[2];
  iVar2 = FUN__text__00419450();
  if (iVar2 == 0) {
    for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
      *(undefined1 *)(local_8 + local_10 + 0x1a95) = *(undefined1 *)(local_c + local_10 + 0x22);
      *(undefined2 *)(local_8 + 0x1a9a + local_10 * 2) =
           *(undefined2 *)(local_c + 0x32 + local_10 * 2);
    }
  }
  else {
    local_18 = FUN__text__0041ac70(*param_1);
    if ((3 < local_18) &&
       (iVar2 = FUN__text__00424f80("pno < 4","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                    DAT_005ffc9c + 8,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined1 *)(local_8 + local_18 + 0x1a95) = *(undefined1 *)(local_c + 0x22);
    *(undefined2 *)(local_8 + 0x1a9a + local_18 * 2) = *(undefined2 *)(local_c + 0x32);
    local_14 = FUN__text__00442f40();
  }
  local_8 = 0x44318d;
  FUN__text__0056ce80();
  return;
}

