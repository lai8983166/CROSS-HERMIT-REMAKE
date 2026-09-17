
void FUN__text__0042d3c0(undefined4 param_1,int param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_2;
  uVar2 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar2;
  iVar3 = FUN__text__00424f80(&DAT_0059507c,&DAT_00595094,DAT_005ff71c + 5,0);
  if (iVar3 == 0) {
    local_8 = 0x42d44f;
    FUN__text__0056ce80();
    return;
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

