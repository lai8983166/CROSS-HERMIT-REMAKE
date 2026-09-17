
void FUN__text__00550cba(void)

{
  int iVar1;
  int in_EAX;
  undefined4 uVar2;
  int iVar3;
  int iVar4;
  char *pcVar5;
  int local_c;
  int local_8;
  
  iVar1 = *(int *)(in_EAX + 0x19c);
  uVar2 = (*(code *)**(undefined4 **)(in_EAX + 4))();
  *(undefined4 *)(iVar1 + 0x10) = uVar2;
  uVar2 = (*(code *)**(undefined4 **)(in_EAX + 4))();
  *(undefined4 *)(iVar1 + 0x14) = uVar2;
  uVar2 = (*(code *)**(undefined4 **)(in_EAX + 4))();
  *(undefined4 *)(iVar1 + 0x18) = uVar2;
  uVar2 = (*(code *)**(undefined4 **)(in_EAX + 4))();
  *(undefined4 *)(iVar1 + 0x1c) = uVar2;
  iVar3 = 0;
  pcVar5 = "7_022_04.mp3";
  local_c = -0xe25100;
  local_8 = -0xb2f480;
  iVar4 = 0x2c8d00;
  do {
    *(int *)(iVar3 + *(int *)(iVar1 + 0x10)) = local_8 >> 0x10;
    *(int *)(iVar3 + *(int *)(iVar1 + 0x14)) = local_c >> 0x10;
    *(char **)(iVar3 + *(int *)(iVar1 + 0x18)) = pcVar5;
    *(int *)(iVar3 + *(int *)(iVar1 + 0x1c)) = iVar4;
    iVar4 = iVar4 + -0x581a;
    pcVar5 = pcVar5 + -0xb6d2;
    iVar3 = iVar3 + 4;
    local_c = local_c + 0x1c5a2;
    local_8 = local_8 + 0x166e9;
  } while (-0x2b34e7 < iVar4);
  return;
}

