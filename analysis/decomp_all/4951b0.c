
void FUN__text__004951b0(int param_1,char param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__00494db0();
  if (local_c != 0) {
    *(undefined2 *)(local_c + 4) = *(undefined2 *)(param_1 + 2);
    *(char *)(local_c + 1) = param_2 + '\x14';
    FUN__text__00495630(local_c);
  }
  local_8 = 0x495218;
  FUN__text__0056ce80();
  return;
}

