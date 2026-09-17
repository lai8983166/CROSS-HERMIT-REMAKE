
void FUN__text__0054fce4(int param_1,char param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  
  puVar2 = (undefined4 *)(*(code *)**(undefined4 **)(param_1 + 4))(param_1,1,0x1c);
  *(undefined4 **)(param_1 + 0x188) = puVar2;
  *puVar2 = &LAB__text__0054fc3e;
  puVar2[2] = 0;
  puVar2[3] = 0;
  if (*(char *)(param_1 + 0x4a) != '\0') {
    uVar3 = *(undefined4 *)(param_1 + 0x110);
    puVar2[4] = uVar3;
    if (param_2 == '\0') {
      uVar3 = (**(code **)(*(int *)(param_1 + 4) + 8))
                        (param_1,1,*(int *)(param_1 + 100) * *(int *)(param_1 + 0x5c),uVar3);
      puVar2[3] = uVar3;
    }
    else {
      iVar1 = *(int *)(param_1 + 4);
      uVar3 = FUN__text__005494c6(*(undefined4 *)(param_1 + 0x60),uVar3,uVar3);
      uVar3 = (**(code **)(iVar1 + 0x10))
                        (param_1,1,0,*(int *)(param_1 + 100) * *(int *)(param_1 + 0x5c),uVar3);
      puVar2[2] = uVar3;
    }
  }
  return;
}

