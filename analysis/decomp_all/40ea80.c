
void FUN__text__0040ea80(int param_1)

{
  size_t sVar1;
  int iVar2;
  undefined4 *puVar3;
  int *piVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_68 [16];
  int *local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int *local_10;
  int local_c;
  
  puVar3 = local_68;
  for (iVar2 = 0x19; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1;
  local_10 = *(int **)(param_1 + 8);
  local_20 = (int)*(short *)(param_1 + 0xc);
  local_1c = (int)*(short *)(param_1 + 0xe);
  local_18 = local_20;
  local_14 = local_1c;
  local_28 = (int *)FUN__text__004142b0();
  uVar6 = *(undefined4 *)(local_c + 0x10);
  uVar5 = 0x100;
  piVar4 = &local_20;
  sVar1 = _strlen((char *)(local_c + 0x14));
  (**(code **)(*local_10 + 0x18))(local_10,local_c + 0x14,sVar1,piVar4,uVar5,uVar6);
  local_24 = FUN__text__0056ce80();
  if (-1 < local_24) {
    (**(code **)(*local_28 + 200))(local_28,0x18,8);
    FUN__text__0056ce80();
    (**(code **)(*local_28 + 200))(local_28,0x19,5);
    FUN__text__0056ce80();
    (**(code **)(*local_28 + 200))(local_28,0x16,1);
    FUN__text__0056ce80();
  }
  local_20 = 0x40eb88;
  FUN__text__0056ce80();
  return;
}

