
void __thiscall FUN__text__00442690(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_2 + 8);
  local_8 = param_1;
  if ((*(char *)(local_c + 0x10) < '\x01') || ('P' < *(char *)(local_c + 0x10))) {
    iVar2 = FUN__text__00424f80("(0<recv->rcnt) && (recv->rcnt<=(20*4))",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\NetMessage.cpp",
                                DAT_005ffc8c + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  _memset((void *)(local_8 + 0x1c30),0,0x3700);
  FUN__text__0056d4d0(local_8 + 0x1c30,local_c + 0x20,*(char *)(local_c + 0x10) * 0xb0);
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    *(undefined1 *)(local_8 + local_10 + 0x1a8c) = *(undefined1 *)(local_c + local_10 + 0x11);
  }
  *(undefined2 *)(local_8 + 0x1aa4) = *(undefined2 *)(local_c + 0x16);
  *(undefined4 *)(local_8 + 0x1aa8) = *(undefined4 *)(local_c + 0x18);
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    *(undefined1 *)(local_8 + local_10 + 0x1aac) = *(undefined1 *)(local_c + local_10 + 0x1c);
  }
  *(undefined1 *)(local_8 + 0x1a90) = 1;
  local_8 = 0x4427c8;
  FUN__text__0056ce80();
  return;
}

