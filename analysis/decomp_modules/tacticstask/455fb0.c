
void FUN__text__00455fb0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(char *)(param_1 + 1) == '\0') {
    if (*(char *)(param_1 + 2) == '\0') {
      if (*(char *)(param_1 + 3) == '\0') {
        FUN__text__00498840((int)*(short *)(param_1 + 4),*(undefined1 *)(param_1 + 6),
                            *(undefined1 *)(param_1 + 7),*(undefined1 *)(param_1 + 8));
      }
      else {
        FUN__text__00498740((int)*(short *)(param_1 + 4),*(undefined1 *)(param_1 + 6),
                            *(undefined1 *)(param_1 + 7));
      }
    }
    else if (*(char *)(param_1 + 3) == '\0') {
      FUN__text__004988d0((int)*(short *)(param_1 + 4),*(undefined1 *)(param_1 + 6),
                          *(undefined1 *)(param_1 + 7),*(undefined1 *)(param_1 + 8));
    }
    else {
      FUN__text__004987c0((int)*(short *)(param_1 + 4),*(undefined1 *)(param_1 + 6),
                          *(undefined1 *)(param_1 + 7));
    }
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp"
                                ,DAT_0060cdb0 + 0xe,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (*(char *)(param_1 + 2) == '\0') {
      if (*(char *)(param_1 + 3) != '\0') {
        FUN__text__00498920((int)*(short *)(param_1 + 4));
      }
    }
    else if (*(char *)(param_1 + 3) != '\0') {
      FUN__text__004989b0((int)*(short *)(param_1 + 4));
    }
  }
  local_8 = 0x456120;
  FUN__text__0056ce80();
  return;
}

