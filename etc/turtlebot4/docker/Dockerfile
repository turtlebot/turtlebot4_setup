FROM ros:humble

# install ros package
RUN apt-get update && apt-get install -y \
      ros-${ROS_DISTRO}-irobot-create-msgs \
      ros-${ROS_DISTRO}-domain-bridge \
      nano && \
    rm -rf /var/lib/apt/lists/*

ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  # [Optional] Add sudo support for the non-root user
  && apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  # Cleanup
  && rm -rf /var/lib/apt/lists/* \
  && echo "source /usr/share/bash-completion/completions/git" >> /home/$USERNAME/.bashrc \
  && echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc


#ENV ROS_WS=/opt/ws
#RUN mkdir -p $ROS_WS/src
#
#WORKDIR $ROS_WS/src
#RUN git clone https://github.com/ros2/domain_bridge.git -b humble
#
#WORKDIR $ROS_WS
#RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
#  colcon build --symlink-install


# #!/bin/bash
# set -e
#
# # setup ros2 environment
# source "/opt/ros/$ROS_DISTRO/setup.bash" --
# exec "$@"
#RUN echo "#!/bin/bash" > /ros_entrypoint.sh && \
#  echo "set -e" >> /ros_entrypoint.sh && \
#  echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /ros_entrypoint.sh && \
#  echo "source $ROS_WS/install/setup.bash" >> /ros_entrypoint.sh && \
#  echo "exec \"\$@\"" >> /ros_entrypoint.sh && \
#  chmod +x /ros_entrypoint.sh
